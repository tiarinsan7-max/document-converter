"""
Workflow Scheduler
Schedule and automate conversion workflows
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from utils.logger import get_logger
from .batch_processor import BatchProcessor, find_files

logger = get_logger(__name__)


class WorkflowScheduler:
    """Schedule and manage conversion workflows"""
    
    def __init__(self, workflows_dir: Optional[Path] = None):
        if workflows_dir is None:
            from config.settings import settings
            workflows_dir = settings.WORKFLOWS_DIR
        
        self.workflows_dir = Path(workflows_dir)
        self.workflows_file = self.workflows_dir / "workflows.json"
        self.processor = BatchProcessor()
    
    def create_workflow(
        self,
        name: str,
        input_dir: str,
        output_dir: str,
        output_format: str,
        quality: str = 'high',
        recursive: bool = False,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new workflow
        
        Args:
            name: Workflow name
            input_dir: Input directory
            output_dir: Output directory
            output_format: Target format
            quality: Conversion quality
            recursive: Process subdirectories
            enabled: Whether workflow is enabled
            
        Returns:
            Workflow configuration
        """
        workflow = {
            'name': name,
            'input_dir': input_dir,
            'output_dir': output_dir,
            'output_format': output_format,
            'quality': quality,
            'recursive': recursive,
            'enabled': enabled,
            'created_at': datetime.now().isoformat(),
            'last_run': None,
            'run_count': 0
        }
        
        # Save workflow
        workflows = self.load_workflows()
        workflows[name] = workflow
        self.save_workflows(workflows)
        
        logger.info(f"Created workflow: {name}")
        return workflow
    
    def run_workflow(self, name: str) -> Dict[str, Any]:
        """
        Run a workflow
        
        Args:
            name: Workflow name
            
        Returns:
            Execution results
        """
        workflows = self.load_workflows()
        
        if name not in workflows:
            raise ValueError(f"Workflow not found: {name}")
        
        workflow = workflows[name]
        
        if not workflow.get('enabled', True):
            logger.warning(f"Workflow is disabled: {name}")
            return {'success': False, 'message': 'Workflow is disabled'}
        
        logger.info(f"Running workflow: {name}")
        
        # Find files
        input_path = Path(workflow['input_dir'])
        files = find_files(
            input_path,
            recursive=workflow.get('recursive', False)
        )
        
        if not files:
            logger.warning(f"No files found for workflow: {name}")
            return {
                'success': True,
                'message': 'No files to process',
                'total_files': 0
            }
        
        # Process batch
        output_path = Path(workflow['output_dir'])
        results = self.processor.process_batch(
            files,
            output_path,
            workflow['output_format'],
            workflow.get('quality', 'high')
        )
        
        # Update workflow stats
        workflow['last_run'] = datetime.now().isoformat()
        workflow['run_count'] = workflow.get('run_count', 0) + 1
        workflows[name] = workflow
        self.save_workflows(workflows)
        
        logger.info(
            f"Workflow completed: {name} - "
            f"{results['successful']}/{results['total_files']} successful"
        )
        
        return results
    
    def run_all_workflows(self) -> Dict[str, Any]:
        """
        Run all enabled workflows
        
        Returns:
            Combined results
        """
        workflows = self.load_workflows()
        results = {}
        
        for name, workflow in workflows.items():
            if workflow.get('enabled', True):
                try:
                    results[name] = self.run_workflow(name)
                except Exception as e:
                    logger.error(f"Failed to run workflow {name}: {e}")
                    results[name] = {
                        'success': False,
                        'error': str(e)
                    }
        
        return results
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all workflows
        
        Returns:
            List of workflows
        """
        workflows = self.load_workflows()
        return list(workflows.values())
    
    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get workflow by name
        
        Args:
            name: Workflow name
            
        Returns:
            Workflow configuration or None
        """
        workflows = self.load_workflows()
        return workflows.get(name)
    
    def delete_workflow(self, name: str) -> bool:
        """
        Delete a workflow
        
        Args:
            name: Workflow name
            
        Returns:
            True if deleted
        """
        workflows = self.load_workflows()
        
        if name in workflows:
            del workflows[name]
            self.save_workflows(workflows)
            logger.info(f"Deleted workflow: {name}")
            return True
        
        return False
    
    def enable_workflow(self, name: str) -> bool:
        """Enable a workflow"""
        return self._set_workflow_enabled(name, True)
    
    def disable_workflow(self, name: str) -> bool:
        """Disable a workflow"""
        return self._set_workflow_enabled(name, False)
    
    def _set_workflow_enabled(self, name: str, enabled: bool) -> bool:
        """Set workflow enabled status"""
        workflows = self.load_workflows()
        
        if name in workflows:
            workflows[name]['enabled'] = enabled
            self.save_workflows(workflows)
            logger.info(f"Workflow {name} {'enabled' if enabled else 'disabled'}")
            return True
        
        return False
    
    def load_workflows(self) -> Dict[str, Any]:
        """Load workflows from file"""
        if not self.workflows_file.exists():
            return {}
        
        try:
            with open(self.workflows_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load workflows: {e}")
            return {}
    
    def save_workflows(self, workflows: Dict[str, Any]):
        """Save workflows to file"""
        try:
            self.workflows_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.workflows_file, 'w', encoding='utf-8') as f:
                json.dump(workflows, f, indent=2, ensure_ascii=False)
            
            logger.info("Workflows saved")
            
        except Exception as e:
            logger.error(f"Failed to save workflows: {e}")
            raise


# Convenience functions
def create_workflow(**kwargs) -> Dict[str, Any]:
    """Create workflow (convenience function)"""
    scheduler = WorkflowScheduler()
    return scheduler.create_workflow(**kwargs)


def run_workflow(name: str) -> Dict[str, Any]:
    """Run workflow (convenience function)"""
    scheduler = WorkflowScheduler()
    return scheduler.run_workflow(name)


def list_workflows() -> List[Dict[str, Any]]:
    """List workflows (convenience function)"""
    scheduler = WorkflowScheduler()
    return scheduler.list_workflows()
