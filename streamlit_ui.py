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
        if st.button("✅ Accept Frontend", type="primary"):
            st.success("Frontend SRD Accepted!")
        
        if st.button("❌ Reject Frontend"):
            st.error("Frontend SRD Rejected!")
    
    st.markdown("---")
    
    # Backend SRD
    st.header("Backend SRD")
    col1, col2 = st.columns([8, 2])
    
    with col1:
        backend_srd = result.get("backend_srd", "No backend SRD generated")
        st.markdown(backend_srd)
    
    with col2:
        if st.button("✅ Accept Backend", type="primary"):
            st.success("Backend SRD Accepted!")
        
        if st.button("❌ Reject Backend"):
            st.error("Backend SRD Rejected!")