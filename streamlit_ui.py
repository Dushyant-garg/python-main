import streamlit as st
import requests
import os
from pathlib import Path
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Requirements Analyzer - SRD Review",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "frontend_status" not in st.session_state:
    st.session_state.frontend_status = "pending"

if "backend_status" not in st.session_state:
    st.session_state.backend_status = "pending"

# API Configuration
API_BASE_URL = "http://localhost:8000"

def upload_and_analyze_document(uploaded_file):
    """Upload document and analyze requirements"""
    try:
        # Upload file
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        with st.spinner("🤖 AI Agents are analyzing your document..."):
            response = requests.post(f"{API_BASE_URL}/analyze-from-upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            st.error(f"Error analyzing document: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        st.info("Make sure the FastAPI backend is running on http://localhost:8000")
        return None

def get_status_color(status):
    """Get color for status display"""
    colors = {
        "pending": "🟡",
        "accepted": "🟢", 
        "rejected": "🔴"
    }
    return colors.get(status, "⚪")

def render_status_badge(status):
    """Render status as colored text"""
    color_map = {
        "pending": "orange",
        "accepted": "green",
        "rejected": "red"
    }
    color = color_map.get(status, "gray")
    return f"<span style='color: {color}; font-weight: bold; text-transform: uppercase;'>{status}</span>"

# Main App Layout
st.title("📋 Requirements Analyzer - SRD Review")
st.markdown("Upload documents, review generated SRDs, and approve or reject them")

# Sidebar for document upload
with st.sidebar:
    st.header("📁 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=["pdf", "docx", "txt"],
        help="Upload a project requirements document (PDF, DOCX, or TXT)"
    )
    
    if uploaded_file and st.button("🔍 Analyze Document", type="primary"):
        st.session_state.uploaded_file_name = uploaded_file.name
        result = upload_and_analyze_document(uploaded_file)
        
        if result:
            st.session_state.analysis_result = result
            st.session_state.frontend_status = "pending"
            st.session_state.backend_status = "pending"
            st.success("✅ Document analyzed successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to analyze document")
    
    if st.session_state.uploaded_file_name:
        st.success(f"📄 Analyzed: {st.session_state.uploaded_file_name}")
    
    st.markdown("---")
    
    # Status Summary
    st.header("📊 Review Status")
    if st.session_state.analysis_result:
        st.markdown(f"**Frontend SRD:** {get_status_color(st.session_state.frontend_status)} {st.session_state.frontend_status.title()}")
        st.markdown(f"**Backend SRD:** {get_status_color(st.session_state.backend_status)} {st.session_state.backend_status.title()}")
        
        # Overall status
        if st.session_state.frontend_status == "accepted" and st.session_state.backend_status == "accepted":
            st.success("🎉 All SRDs Accepted!")
        elif "rejected" in [st.session_state.frontend_status, st.session_state.backend_status]:
            st.error("❌ Some SRDs Rejected")
        else:
            st.info("⏳ Pending Review")
    
    st.markdown("---")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    if st.session_state.analysis_result:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Accept All", help="Accept both Frontend and Backend SRDs"):
                st.session_state.frontend_status = "accepted"
                st.session_state.backend_status = "accepted"
                st.success("All SRDs accepted!")
                st.rerun()
        
        with col2:
            if st.button("❌ Reject All", help="Reject both Frontend and Backend SRDs"):
                st.session_state.frontend_status = "rejected"
                st.session_state.backend_status = "rejected"
                st.error("All SRDs rejected!")
                st.rerun()

# Main content area
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    # Create tabs for different SRDs
    tab1, tab2, tab3 = st.tabs(["🎨 Frontend SRD", "⚙️ Backend SRD", "📊 Analysis Summary"])
    
    with tab1:
        # Frontend SRD Header
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.subheader("Frontend Software Requirements Document")
        
        with col2:
            st.markdown(f"**Status:** {render_status_badge(st.session_state.frontend_status)}", unsafe_allow_html=True)
        
        with col3:
            if st.button("✅ Accept", key="accept_frontend", type="primary", disabled=st.session_state.frontend_status == "accepted"):
                st.session_state.frontend_status = "accepted"
                st.success("Frontend SRD accepted! ✅")
                time.sleep(1)
                st.rerun()
        
        with col4:
            if st.button("❌ Reject", key="reject_frontend", disabled=st.session_state.frontend_status == "rejected"):
                st.session_state.frontend_status = "rejected"
                st.error("Frontend SRD rejected! ❌")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        
        # Display Frontend SRD content
        frontend_srd = result.get("frontend_srd", "No frontend SRD generated")
        st.markdown(frontend_srd)
    
    with tab2:
        # Backend SRD Header
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.subheader("Backend Software Requirements Document")
        
        with col2:
            st.markdown(f"**Status:** {render_status_badge(st.session_state.backend_status)}", unsafe_allow_html=True)
        
        with col3:
            if st.button("✅ Accept", key="accept_backend", type="primary", disabled=st.session_state.backend_status == "accepted"):
                st.session_state.backend_status = "accepted"
                st.success("Backend SRD accepted! ✅")
                time.sleep(1)
                st.rerun()
        
        with col4:
            if st.button("❌ Reject", key="reject_backend", disabled=st.session_state.backend_status == "rejected"):
                st.session_state.backend_status = "rejected"
                st.error("Backend SRD rejected! ❌")
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        
        # Display Backend SRD content
        backend_srd = result.get("backend_srd", "No backend SRD generated")
        st.markdown(backend_srd)
    
    with tab3:
        st.subheader("Requirements Analysis Summary")
        
        # Show analysis summary if available
        analysis_summary = result.get("analysis_summary", "")
        if analysis_summary:
            st.markdown("**AI Agent Analysis:**")
            st.info(analysis_summary)
        
        # Show file paths
        frontend_path = result.get("frontend_srd_path", "")
        backend_path = result.get("backend_srd_path", "")
        
        if frontend_path or backend_path:
            st.markdown("**Generated Files:**")
            if frontend_path:
                st.text(f"📄 Frontend SRD: {frontend_path}")
            if backend_path:
                st.text(f"📄 Backend SRD: {backend_path}")
        
        # Show raw response for debugging
        with st.expander("🔍 Raw API Response (Debug)"):
            st.json(result)
    
    # Action Summary at the bottom
    st.markdown("---")
    
    # Show final summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Frontend SRD",
            value=st.session_state.frontend_status.title(),
            delta="✅ Approved" if st.session_state.frontend_status == "accepted" else "❌ Rejected" if st.session_state.frontend_status == "rejected" else "⏳ Pending"
        )
    
    with col2:
        st.metric(
            label="Backend SRD", 
            value=st.session_state.backend_status.title(),
            delta="✅ Approved" if st.session_state.backend_status == "accepted" else "❌ Rejected" if st.session_state.backend_status == "rejected" else "⏳ Pending"
        )
    
    with col3:
        overall_status = "Complete" if all(status == "accepted" for status in [st.session_state.frontend_status, st.session_state.backend_status]) else "Incomplete"
        st.metric(
            label="Overall Status",
            value=overall_status,
            delta="🎉 All Approved!" if overall_status == "Complete" else "⏳ Review Needed"
        )
    
else:
    # Welcome screen when no document is uploaded
    st.markdown("""
    ## 🚀 Welcome to Requirements Analyzer
    
    This tool helps you review AI-generated Software Requirements Documents (SRDs).
    
    ### How it works:
    1. **📤 Upload** a requirements document using the sidebar
    2. **🤖 AI Analysis** - Three specialized agents analyze your document:
       - 📊 **Requirements Analyst** - Categorizes requirements  
       - 🎨 **Frontend Specialist** - Creates frontend SRD
       - ⚙️ **Backend Specialist** - Creates backend SRD
    3. **📋 Review** the generated SRDs in separate tabs
    4. **✅ Accept** or **❌ Reject** each SRD individually
    
    ### Supported Formats:
    - 📄 **PDF** documents
    - 📝 **DOCX** Word documents  
    - 📋 **TXT** text files
    
    ### Features:
    - 🎯 **Separate SRDs** for frontend and backend concerns
    - 📊 **Status tracking** for each document
    - ⚡ **Quick actions** to accept/reject all at once
    - 🔍 **Detailed analysis** from AI agents
    
    ---
    
    **👈 Start by uploading a document in the sidebar**
    """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, FastAPI, and AutoGen AI Agents*")

# Add some CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
    }
    
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    
    .stTab {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)