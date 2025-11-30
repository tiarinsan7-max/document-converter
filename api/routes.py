"""
API Routes
FastAPI route handlers for document conversion
"""

import time
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from converters import ConverterFactory, get_supported_formats, get_supported_conversions
from utils.file_handler import FileHandler
from utils.validators import validate_file
from utils.errors import ConversionError, FileValidationError, UnsupportedFormatError
from utils.logger import get_logger
from utils.helpers import get_file_size, format_file_size
from .models import (
    ConversionResponse,
    ErrorResponse,
    FormatsResponse,
    BatchConversionResponse,
    HealthResponse
)
from config.settings import settings

logger = get_logger(__name__)
router = APIRouter()

# Initialize services
factory = ConverterFactory()
file_handler = FileHandler()

# Track uptime
start_time = time.time()


@router.post("/convert", response_model=ConversionResponse)
async def convert_file(
    file: UploadFile = File(..., description="File to convert"),
    output_format: str = Form(..., description="Target output format"),
    quality: str = Form(default="high", description="Conversion quality (low, medium, high)")
):
    """
    Convert a single file to target format
    
    - **file**: Upload file to convert
    - **output_format**: Target format (pdf, docx, xlsx, csv, json, txt)
    - **quality**: Conversion quality (low, medium, high)
    """
    start_time_conv = time.time()
    temp_input = None
    temp_output = None
    
    try:
        # Save uploaded file
        file_content = await file.read()
        temp_input = await file_handler.save_upload_async(
            file_content,
            file.filename
        )
        
        # Validate file
        is_valid, error = validate_file(temp_input)
        if not is_valid:
            raise FileValidationError(error, file.filename)
        
        # Get input format
        input_format = temp_input.suffix.lower().replace('.', '')
        
        # Check if conversion is supported
        if not factory.supports_conversion(input_format, output_format):
            raise UnsupportedFormatError(
                f"{input_format} to {output_format}",
                get_supported_formats()
            )
        
        # Generate output path
        temp_output = file_handler.get_output_path(
            temp_input,
            output_format
        )
        
        # Perform conversion
        logger.info(f"Converting {file.filename} to {output_format}")
        result = factory.convert(temp_input, temp_output, quality=quality)
        
        # Get file info
        output_size = get_file_size(result)
        conversion_time = time.time() - start_time_conv
        
        # Generate download URL
        download_url = f"/download/{result.name}"
        
        return ConversionResponse(
            message="Conversion completed successfully",
            input_file=file.filename,
            output_file=result.name,
            output_format=output_format,
            file_size=output_size,
            download_url=download_url,
            conversion_time=round(conversion_time, 2)
        )
        
    except (FileValidationError, UnsupportedFormatError, ConversionError) as e:
        logger.error(f"Conversion failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        
    finally:
        # Cleanup input file
        if temp_input and temp_input.exists():
            file_handler.delete_file(temp_input)


@router.post("/batch-convert", response_model=BatchConversionResponse)
async def batch_convert(
    files: List[UploadFile] = File(..., description="Files to convert"),
    output_format: str = Form(..., description="Target output format"),
    quality: str = Form(default="high", description="Conversion quality")
):
    """
    Convert multiple files to target format
    
    - **files**: List of files to convert
    - **output_format**: Target format for all files
    - **quality**: Conversion quality
    """
    start_time_batch = time.time()
    results = []
    successful = 0
    failed = 0
    
    for file in files:
        temp_input = None
        try:
            # Save uploaded file
            file_content = await file.read()
            temp_input = await file_handler.save_upload_async(
                file_content,
                file.filename
            )
            
            # Validate and convert
            is_valid, error = validate_file(temp_input)
            if not is_valid:
                raise FileValidationError(error, file.filename)
            
            input_format = temp_input.suffix.lower().replace('.', '')
            
            if not factory.supports_conversion(input_format, output_format):
                raise UnsupportedFormatError(f"{input_format} to {output_format}")
            
            temp_output = file_handler.get_output_path(temp_input, output_format)
            result = factory.convert(temp_input, temp_output, quality=quality)
            
            successful += 1
            results.append({
                "filename": file.filename,
                "status": "success",
                "output_file": result.name,
                "download_url": f"/download/{result.name}"
            })
            
        except Exception as e:
            failed += 1
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
            logger.error(f"Failed to convert {file.filename}: {e}")
            
        finally:
            if temp_input and temp_input.exists():
                file_handler.delete_file(temp_input)
    
    total_time = time.time() - start_time_batch
    
    return BatchConversionResponse(
        message=f"Batch conversion completed: {successful} successful, {failed} failed",
        total_files=len(files),
        successful=successful,
        failed=failed,
        results=results,
        total_time=round(total_time, 2)
    )


@router.get("/download/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    """
    Download converted file
    
    - **filename**: Name of the file to download
    """
    file_path = settings.OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Schedule file deletion after download
    background_tasks.add_task(file_handler.delete_file, file_path)
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@router.get("/formats", response_model=FormatsResponse)
async def get_formats():
    """
    Get list of supported formats and conversion matrix
    """
    formats = get_supported_formats()
    conversions = factory.get_all_conversions()
    
    return FormatsResponse(
        formats=formats,
        total=len(formats),
        conversions=conversions
    )


@router.get("/formats/{format_name}")
async def get_format_conversions(format_name: str):
    """
    Get supported conversions for specific format
    
    - **format_name**: Format to query (e.g., 'pdf', 'docx')
    """
    format_name = format_name.lower()
    
    if format_name not in get_supported_formats():
        raise HTTPException(
            status_code=404,
            detail=f"Format '{format_name}' not supported"
        )
    
    conversions = get_supported_conversions(format_name)
    
    return {
        "format": format_name,
        "supported_conversions": conversions,
        "total": len(conversions)
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        uptime=round(uptime, 2),
        supported_formats=len(get_supported_formats())
    )


@router.delete("/cleanup")
async def cleanup_files():
    """
    Cleanup old temporary files
    """
    try:
        deleted_uploads = file_handler.cleanup_temp_files(max_age_hours=24)
        
        # Also clean output directory
        from utils.helpers import clean_directory
        clean_directory(settings.OUTPUT_DIR, pattern='*')
        
        return {
            "success": True,
            "message": f"Cleaned up {deleted_uploads} temporary files"
        }
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs_url": "/docs",
        "supported_formats": get_supported_formats()
    }
