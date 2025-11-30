"""
Workflows Page
Manage and run conversion workflows
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Workflows import WorkflowScheduler, list_workflows

st.set_page_config(
    page_title="Workflows - Document Converter",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Conversion Workflows")
st.markdown("Create and manage automated conversion workflows")

# Initialize scheduler
scheduler = WorkflowScheduler()

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Create Workflow", "▶️ Run Workflows", "📊 Manage Workflows"])

with tab1:
    st.header("Create New Workflow")
    
    with st.form("create_workflow"):
        col1, col2 = st.columns(2)
        
        with col1:
            workflow_name = st.text_input(
                "Workflow Name",
                placeholder="e.g., daily_pdf_conversion"
            )
            
            input_dir = st.text_input(
                "Input Directory",
                placeholder="/path/to/input"
            )
            
            output_format = st.selectbox(
                "Output Format",
                ["pdf", "docx", "xlsx", "csv", "json", "txt"]
            )
        
        with col2:
            output_dir = st.text_input(
                "Output Directory",
                placeholder="/path/to/output"
            )
            
            quality = st.select_slider(
                "Quality",
                options=["low", "medium", "high"],
                value="high"
            )
            
            recursive = st.checkbox("Process subdirectories", value=False)
        
        submitted = st.form_submit_button("Create Workflow", type="primary")
        
        if submitted:
            if workflow_name and input_dir and output_dir:
                try:
                    workflow = scheduler.create_workflow(
                        name=workflow_name,
                        input_dir=input_dir,
                        output_dir=output_dir,
                        output_format=output_format,
                        quality=quality,
                        recursive=recursive
                    )
                    st.success(f"✅ Workflow '{workflow_name}' created successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to create workflow: {e}")
            else:
                st.warning("⚠️ Please fill in all required fields")

with tab2:
    st.header("Run Workflows")
    
    workflows = list_workflows()
    
    if workflows:
        for workflow in workflows:
            with st.expander(f"📋 {workflow['name']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.text(f"Input: {workflow['input_dir']}")
                    st.text(f"Output: {workflow['output_dir']}")
                
                with col2:
                    st.text(f"Format: {workflow['output_format'].upper()}")
                    st.text(f"Quality: {workflow['quality']}")
                
                with col3:
                    st.text(f"Runs: {workflow.get('run_count', 0)}")
                    enabled = workflow.get('enabled', True)
                    st.text(f"Status: {'✅ Enabled' if enabled else '❌ Disabled'}")
                
                if enabled:
                    if st.button(f"▶️ Run {workflow['name']}", key=f"run_{workflow['name']}"):
                        with st.spinner(f"Running workflow '{workflow['name']}'..."):
                            try:
                                results = scheduler.run_workflow(workflow['name'])
                                
                                if results.get('success', True):
                                    st.success(
                                        f"✅ Workflow completed! "
                                        f"{results.get('successful', 0)}/{results.get('total_files', 0)} files converted"
                                    )
                                else:
                                    st.error(f"❌ Workflow failed: {results.get('message', 'Unknown error')}")
                            except Exception as e:
                                st.error(f"❌ Error: {e}")
    else:
        st.info("📝 No workflows created yet. Create one in the 'Create Workflow' tab.")

with tab3:
    st.header("Manage Workflows")
    
    workflows = list_workflows()
    
    if workflows:
        for workflow in workflows:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.subheader(workflow['name'])
                    st.caption(f"Created: {workflow.get('created_at', 'Unknown')}")
                
                with col2:
                    enabled = workflow.get('enabled', True)
                    if enabled:
                        if st.button("Disable", key=f"disable_{workflow['name']}"):
                            scheduler.disable_workflow(workflow['name'])
                            st.rerun()
                    else:
                        if st.button("Enable", key=f"enable_{workflow['name']}"):
                            scheduler.enable_workflow(workflow['name'])
                            st.rerun()
                
                with col3:
                    if st.button("📊 Details", key=f"details_{workflow['name']}"):
                        st.json(workflow)
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{workflow['name']}"):
                        if scheduler.delete_workflow(workflow['name']):
                            st.success(f"Deleted workflow: {workflow['name']}")
                            st.rerun()
                
                st.divider()
    else:
        st.info("📝 No workflows to manage")
