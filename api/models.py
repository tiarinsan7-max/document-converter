"""
API Data Models
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ConversionRequest(BaseModel):
    """Request model for file conversion"""
    output_format: str = Field(..., description="Target output format")
    quality: str = Field(default="high", description="Conversion quality (low, medium, high)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "output_format": "docx",
                "quality": "high"
            }
        }


class ConversionResponse(BaseModel):
    """Response model for successful conversion"""
    success: bool = Field(default=True)
    message: str = Field(..., description="Success message")
    input_file: str = Field(..., description="Original filename")
    output_file: str = Field(..., description="Converted filename")
    output_format: str = Field(..., description="Output format")
    file_size: int = Field(..., description="Output file size in bytes")
    download_url: str = Field(..., description="URL to download converted file")
    conversion_time: float = Field(..., description="Conversion time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Conversion completed successfully",
                "input_file": "document.pdf",
                "output_file": "document.docx",
                "output_format": "docx",
                "file_size": 45678,
                "download_url": "/download/document.docx",
                "conversion_time": 2.34
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors"""
    success: bool = Field(default=False)
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "ConversionError",
                "message": "Failed to convert file",
                "details": {
                    "input_file": "document.pdf",
                    "output_format": "docx"
                }
            }
        }


class FormatInfo(BaseModel):
    """Information about a file format"""
    format: str = Field(..., description="Format name")
    extensions: List[str] = Field(..., description="File extensions")
    description: str = Field(..., description="Format description")
    supported_conversions: List[str] = Field(..., description="Supported output formats")


class FormatsResponse(BaseModel):
    """Response model for supported formats"""
    formats: List[str] = Field(..., description="List of supported formats")
    total: int = Field(..., description="Total number of formats")
    conversions: Dict[str, List[str]] = Field(..., description="Conversion matrix")


class BatchConversionRequest(BaseModel):
    """Request model for batch conversion"""
    output_format: str = Field(..., description="Target output format")
    quality: str = Field(default="high", description="Conversion quality")
    
    class Config:
        json_schema_extra = {
            "example": {
                "output_format": "pdf",
                "quality": "high"
            }
        }


class BatchConversionResponse(BaseModel):
    """Response model for batch conversion"""
    success: bool = Field(default=True)
    message: str = Field(..., description="Status message")
    total_files: int = Field(..., description="Total files processed")
    successful: int = Field(..., description="Successfully converted files")
    failed: int = Field(..., description="Failed conversions")
    results: List[Dict[str, Any]] = Field(..., description="Individual conversion results")
    total_time: float = Field(..., description="Total processing time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Batch conversion completed",
                "total_files": 10,
                "successful": 9,
                "failed": 1,
                "results": [],
                "total_time": 15.67
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Uptime in seconds")
    supported_formats: int = Field(..., description="Number of supported formats")


class FileInfo(BaseModel):
    """File information model"""
    filename: str
    size: int
    format: str
    mime_type: Optional[str] = None
    created_at: Optional[datetime] = None
