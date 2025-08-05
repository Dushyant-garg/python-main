import streamlit as st
import requests

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