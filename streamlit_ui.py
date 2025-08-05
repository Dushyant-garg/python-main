import streamlit as st
import requests
import os

# Configure Streamlit page
st.set_page_config(
    page_title="SRD Review",
    page_icon="📋",
    layout="wide"
)

# Session state initialization
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# API Configuration
API_BASE_URL = "http://localhost:8000"

def upload_and_analyze_document(uploaded_file):
    """Upload document and analyze requirements"""
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        with st.spinner("Analyzing document..."):
            response = requests.post(f"{API_BASE_URL}/analyze-from-upload", files=files)
        
        if response.status_code == 200:
            analysis_result = response.json()
            
            # Fetch the actual SRD content
            frontend_response = requests.get(f"{API_BASE_URL}/srd-content/frontend")
            backend_response = requests.get(f"{API_BASE_URL}/srd-content/backend")
            
            if frontend_response.status_code == 200:
                analysis_result["frontend_srd"] = frontend_response.json()["content"]
            else:
                analysis_result["frontend_srd"] = "Frontend SRD not available"
                
            if backend_response.status_code == 200:
                analysis_result["backend_srd"] = backend_response.json()["content"]
            else:
                analysis_result["backend_srd"] = "Backend SRD not available"
            
            return analysis_result
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Main App
st.title("📋 SRD Review")

# File upload
uploaded_file = st.file_uploader("Upload document", type=["pdf", "docx", "txt"])

if uploaded_file and st.button("Analyze Document"):
    result = upload_and_analyze_document(uploaded_file)
    if result:
        st.session_state.analysis_result = result
        st.success("Document analyzed!")

# Function to regenerate SRD with feedback
def regenerate_srd(srd_type, feedback, original_result):
    """Regenerate SRD with user feedback"""
    try:
        payload = {
            "srd_type": srd_type,
            "feedback": feedback,
            "original_analysis": original_result.get("analysis_summary", "")
        }
        
        response = requests.post(f"{API_BASE_URL}/regenerate-srd", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error regenerating SRD: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def generate_backend_code(backend_srd, project_name):
    """Generate backend code from SRD"""
    try:
        payload = {
            "backend_srd": backend_srd,
            "project_name": project_name,
            "output_format": "files"
        }
        
        with st.spinner("Generating backend code..."):
            response = requests.post(f"{API_BASE_URL}/generate-backend-code", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error generating code: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def generate_frontend_code(frontend_srd, project_name):
    """Generate Angular frontend code from SRD"""
    try:
        payload = {
            "frontend_srd": frontend_srd,
            "project_name": project_name,
            "framework": "angular",
            "output_format": "files"
        }
        
        with st.spinner("Generating Angular frontend code..."):
            response = requests.post(f"{API_BASE_URL}/generate-frontend-code", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error generating frontend code: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Initialize session state for feedback
if "show_frontend_feedback" not in st.session_state:
    st.session_state.show_frontend_feedback = False
if "show_backend_feedback" not in st.session_state:
    st.session_state.show_backend_feedback = False

# Show SRDs if available
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    # Frontend SRD
    st.header("Frontend SRD")
    col1, col2 = st.columns([8, 2])
    
    with col1:
        frontend_srd = result.get("frontend_srd", "No frontend SRD generated")
        st.markdown(frontend_srd)
    
    with col2:
        if st.button("✅ Accept Frontend", type="primary", key="accept_frontend"):
            st.success("Frontend SRD Accepted!")
        
        if st.button("❌ Reject Frontend", key="reject_frontend"):
            st.session_state.show_frontend_feedback = True
    
    # Frontend feedback section
    if st.session_state.show_frontend_feedback:
        with st.expander("🔍 Frontend Feedback", expanded=True):
            frontend_feedback = st.text_area(
                "What needs to be improved in the Frontend SRD?",
                placeholder="Please specify what changes you'd like to see in the frontend requirements...",
                key="frontend_feedback_input",
                height=100
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🔄 Regenerate Frontend", type="primary"):
                    if frontend_feedback.strip():
                        with st.spinner("Regenerating Frontend SRD..."):
                            regenerated = regenerate_srd("frontend", frontend_feedback, result)
                            if regenerated:
                                st.session_state.analysis_result["frontend_srd"] = regenerated["frontend_srd"]
                                st.session_state.show_frontend_feedback = False
                                st.rerun()
                    else:
                        st.error("Please provide feedback before regenerating")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_frontend_feedback = False
                    st.rerun()
    
    # Frontend Code Generation Section
    if result.get("frontend_srd"):
        st.markdown("---")
        st.header("🎨 Frontend Code Generation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            frontend_project_name = st.text_input(
                "Frontend Project Name", 
                value="my_angular_app",
                help="Name for your generated Angular project",
                key="frontend_project_name"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("🎨 Generate Angular Code", type="secondary", key="generate_frontend"):
                if frontend_project_name.strip():
                    frontend_code_result = generate_frontend_code(result["frontend_srd"], frontend_project_name.strip())
                    if frontend_code_result and frontend_code_result.get("success"):
                        st.session_state.generated_frontend_code = frontend_code_result
                        st.success(f"✅ {frontend_code_result['message']}")
                        st.balloons()
                    else:
                        st.error("Failed to generate frontend code")
                else:
                    st.error("Please enter a frontend project name")
    else:
        st.info("Frontend SRD must be generated first before frontend code generation")
    
    st.markdown("---")
    
    # Backend SRD
    st.header("Backend SRD")
    col1, col2 = st.columns([8, 2])
    
    with col1:
        backend_srd = result.get("backend_srd", "No backend SRD generated")
        st.markdown(backend_srd)
    
    with col2:
        if st.button("✅ Accept Backend", type="primary", key="accept_backend"):
            st.success("Backend SRD Accepted!")
        
        if st.button("❌ Reject Backend", key="reject_backend"):
            st.session_state.show_backend_feedback = True
    
    # Backend feedback section
    if st.session_state.show_backend_feedback:
        with st.expander("🔍 Backend Feedback", expanded=True):
            backend_feedback = st.text_area(
                "What needs to be improved in the Backend SRD?",
                placeholder="Please specify what changes you'd like to see in the backend requirements...",
                key="backend_feedback_input",
                height=100
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🔄 Regenerate Backend", type="primary"):
                    if backend_feedback.strip():
                        with st.spinner("Regenerating Backend SRD..."):
                            regenerated = regenerate_srd("backend", backend_feedback, result)
                            if regenerated:
                                st.session_state.analysis_result["backend_srd"] = regenerated["backend_srd"]
                                st.session_state.show_backend_feedback = False
                                st.rerun()
                    else:
                        st.error("Please provide feedback before regenerating")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_backend_feedback = False
                    st.rerun()
    
    # Code Generation Section
    st.markdown("---")
    st.header("🚀 Backend Code Generation")
    
    if result.get("backend_srd"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            project_name = st.text_input(
                "Project Name", 
                value="my_backend_project",
                help="Name for your generated backend project"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("🔨 Generate Backend Code", type="primary"):
                if project_name.strip():
                    code_result = generate_backend_code(result["backend_srd"], project_name.strip())
                    if code_result and code_result.get("success"):
                        st.session_state.generated_code = code_result
                        st.success(f"✅ {code_result['message']}")
                        st.balloons()
                    else:
                        st.error("Failed to generate backend code")
                else:
                    st.error("Please enter a project name")
    else:
        st.info("Backend SRD must be generated first before code generation")

# Display Generated Code
if st.session_state.get("generated_code"):
    code_result = st.session_state.generated_code
    
    st.markdown("---")
    st.header("📁 Generated Backend Code")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.success(f"📊 Generated {code_result.get('file_count', 0)} files")
        if code_result.get('project_path'):
            st.info(f"📂 Project saved to: `{code_result['project_path']}`")
    
    with col2:
        if st.button("📥 Download ZIP"):
            # This would trigger a download - implementation depends on your deployment
            st.info("Download feature available via API")
    
    with col3:
        if st.button("🔄 Generate Again"):
            st.session_state.generated_code = None
            st.rerun()
    
    # Show generated files
    if code_result.get("generated_files"):
        st.subheader("Generated Files Preview")
        
        # Create tabs for different files
        file_names = list(code_result["generated_files"].keys())
        if file_names:
            # Limit to first 5 files for display
            display_files = file_names[:5]
            tabs = st.tabs([os.path.basename(f) for f in display_files])
            
            for i, file_path in enumerate(display_files):
                with tabs[i]:
                    file_content = code_result["generated_files"][file_path]
                    
                    # Determine file type for syntax highlighting
                    if file_path.endswith('.py'):
                        st.code(file_content, language='python')
                    elif file_path.endswith('.md'):
                        st.markdown(file_content)
                    elif file_path.endswith(('.yml', '.yaml')):
                        st.code(file_content, language='yaml')
                    elif file_path.endswith('.txt'):
                        st.text(file_content)
                    else:
                        st.code(file_content)
            
            if len(file_names) > 5:
                st.info(f"Showing first 5 files. Total files generated: {len(file_names)}")
        
        # Agent contribution summary
        st.subheader("🤖 Multi-Agent Contributions")
        st.info("""
        **Generated by specialized agents:**
        - 🏗️ **APIDesignerAgent**: REST endpoints and routing
        - 📊 **ModelDeveloperAgent**: Database models and schemas  
        - 🧠 **BusinessLogicAgent**: Core business functionality
        - 🔗 **IntegrationAgent**: External service connections
        - 🗃️ **DatabaseMigrationAgent**: Database setup and migrations
        - 🎯 **CodeCoordinatorAgent**: Project structure and integration
        """)

# Display Generated Frontend Code
if st.session_state.get("generated_frontend_code"):
    frontend_code_result = st.session_state.generated_frontend_code
    
    st.markdown("---")
    st.header("🎨 Generated Angular Frontend Code")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.success(f"📊 Generated {frontend_code_result.get('file_count', 0)} Angular files")
        if frontend_code_result.get('project_path'):
            st.info(f"📂 Angular project saved to: `{frontend_code_result['project_path']}`")
        st.info(f"🏗️ Framework: {frontend_code_result.get('framework', 'Angular').title()}")
    
    with col2:
        if st.button("📥 Download Angular ZIP", key="download_frontend"):
            st.info("Frontend download feature available via API")
    
    with col3:
        if st.button("🔄 Generate Frontend Again", key="regenerate_frontend"):
            st.session_state.generated_frontend_code = None
            st.rerun()
    
    # Show generated Angular files
    if frontend_code_result.get("generated_files"):
        st.subheader("Generated Angular Files Preview")
        
        # Create tabs for different file types
        file_names = list(frontend_code_result["generated_files"].keys())
        if file_names:
            # Categorize files for better organization
            ts_files = [f for f in file_names if f.endswith('.ts')]
            html_files = [f for f in file_names if f.endswith('.html')]
            scss_files = [f for f in file_names if f.endswith('.scss')]
            json_files = [f for f in file_names if f.endswith('.json')]
            other_files = [f for f in file_names if not any(f.endswith(ext) for ext in ['.ts', '.html', '.scss', '.json'])]
            
            # Show first few files from each category
            display_files = ts_files[:2] + html_files[:2] + scss_files[:1] + json_files[:1] + other_files[:1]
            display_files = display_files[:6]  # Limit to 6 tabs
            
            if display_files:
                tabs = st.tabs([os.path.basename(f) for f in display_files])
                
                for i, file_path in enumerate(display_files):
                    with tabs[i]:
                        file_content = frontend_code_result["generated_files"][file_path]
                        
                        # Determine file type for syntax highlighting
                        if file_path.endswith('.ts'):
                            st.code(file_content, language='typescript')
                        elif file_path.endswith('.html'):
                            st.code(file_content, language='html')
                        elif file_path.endswith('.scss'):
                            st.code(file_content, language='scss')
                        elif file_path.endswith('.json'):
                            st.code(file_content, language='json')
                        elif file_path.endswith('.md'):
                            st.markdown(file_content)
                        else:
                            st.code(file_content)
                
                if len(file_names) > 6:
                    st.info(f"Showing first 6 files. Total Angular files generated: {len(file_names)}")
                
                # File type breakdown
                file_breakdown = f"""
                **File Type Breakdown:**
                - 📝 TypeScript files: {len(ts_files)}
                - 🎨 HTML templates: {len(html_files)}
                - 💄 SCSS styles: {len(scss_files)}
                - ⚙️ JSON configs: {len(json_files)}
                - 📄 Other files: {len(other_files)}
                """
                st.info(file_breakdown)
        
        # Angular agent contribution summary
        st.subheader("🤖 Angular Multi-Agent Contributions")
        st.info("""
        **Generated by specialized Angular agents:**
        - 🏗️ **ComponentDesignerAgent**: Angular components and TypeScript structure
        - 🔧 **ServiceDeveloperAgent**: Angular services and HTTP clients
        - 🎨 **UIImplementationAgent**: Templates, styles, and Angular Material UI
        - 🗄️ **StateManagementAgent**: NgRx state management and reactive patterns
        - 🎯 **FrontendCoordinatorAgent**: Angular project structure and configuration
        """)