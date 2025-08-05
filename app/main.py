from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict

from app.document_parser import DocumentParser
from app.agents.requirement_analyzer import RequirementAnalyzer
from app.models import (
    DocumentAnalysisRequest, 
    DocumentAnalysisResponse, 
    SRDContent,
    UploadResponse,
    RegenerateSRDRequest,
    RegenerateSRDResponse
)

# Create FastAPI app
app = FastAPI(
    title="Requirements Analyzer API",
    description="API for analyzing project documents and generating Software Requirements Documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_parser = DocumentParser()
requirement_analyzer = RequirementAnalyzer()

# Create upload directory
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Requirements Analyzer API", 
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload-document",
            "analyze": "/analyze-requirements",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Requirements Analyzer"}

@app.post("/upload-document", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for analysis
    
    Supported formats: PDF, DOCX, TXT
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the document to get a preview
        parsed_text = await document_parser.parse_document(file_path)
        preview = parsed_text[:500] + "..." if len(parsed_text) > 500 else parsed_text
        
        return UploadResponse(
            success=True,
            message="Document uploaded successfully",
            file_path=file_path,
            parsed_text_preview=preview
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@app.post("/analyze-requirements", response_model=DocumentAnalysisResponse)
async def analyze_requirements(request: DocumentAnalysisRequest):
    """
    Analyze uploaded document and generate SRDs
    
    This endpoint processes the document and generates both frontend and backend
    Software Requirements Documents using AI agents.
    """
    try:
        # Check if file exists
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="Document file not found")
        
        # Parse the document
        parsed_text = await document_parser.parse_document(request.file_path)
        
        if not parsed_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in document")
        
        # Analyze requirements and generate SRDs
        srd_content = await requirement_analyzer.analyze_requirements(parsed_text)
        
        # Save SRDs to files
        frontend_path, backend_path = await requirement_analyzer.save_srds(
            srd_content, 
            request.output_directory
        )
        
        # Create analysis summary
        analysis_summary = srd_content["analysis"][:1000] + "..." if len(srd_content["analysis"]) > 1000 else srd_content["analysis"]
        
        return DocumentAnalysisResponse(
            success=True,
            message="Requirements analysis completed successfully",
            frontend_srd_path=frontend_path,
            backend_srd_path=backend_path,
            analysis_summary=analysis_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing requirements: {str(e)}")

@app.post("/analyze-from-upload", response_model=DocumentAnalysisResponse)
async def analyze_from_upload(
    file: UploadFile = File(...),
    output_directory: str = "output"
):
    """
    Upload and analyze document in one step
    
    This is a convenience endpoint that combines upload and analysis.
    """
    try:
        # Upload the document first
        upload_response = await upload_document(file)
        
        if not upload_response.success:
            raise HTTPException(status_code=400, detail="Failed to upload document")
        
        # Create analysis request
        analysis_request = DocumentAnalysisRequest(
            file_path=upload_response.file_path,
            output_directory=output_directory
        )
        
        # Analyze the document
        return await analyze_requirements(analysis_request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in combined upload and analysis: {str(e)}")

@app.get("/srd-content/{file_type}")
async def get_srd_content(file_type: str, output_dir: str = "output"):
    """
    Retrieve generated SRD content
    
    Args:
        file_type: Either 'frontend' or 'backend'
        output_dir: Directory where SRDs are stored
    """
    try:
        if file_type not in ['frontend', 'backend']:
            raise HTTPException(status_code=400, detail="file_type must be 'frontend' or 'backend'")
        
        file_path = os.path.join(output_dir, f"srd_{file_type}.md")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"SRD file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {"content": content, "file_path": file_path}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving SRD content: {str(e)}")

@app.post("/regenerate-srd", response_model=RegenerateSRDResponse)
async def regenerate_srd(request: RegenerateSRDRequest):
    """
    Regenerate SRD based on user feedback
    
    Args:
        request: Contains srd_type, feedback, and original analysis
    """
    try:
        if request.srd_type not in ['frontend', 'backend']:
            raise HTTPException(status_code=400, detail="srd_type must be 'frontend' or 'backend'")
        
        if not request.feedback.strip():
            raise HTTPException(status_code=400, detail="Feedback cannot be empty")
        
        # Regenerate the SRD with feedback
        result = await requirement_analyzer.regenerate_srd_with_feedback(
            srd_type=request.srd_type,
            feedback=request.feedback,
            original_analysis=request.original_analysis or ""
        )
        
        # Save the regenerated SRD to file
        if request.srd_type == "frontend" and "frontend_srd" in result:
            output_dir = "output"
            Path(output_dir).mkdir(exist_ok=True)
            file_path = os.path.join(output_dir, "srd_frontend.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result["frontend_srd"])
        elif request.srd_type == "backend" and "backend_srd" in result:
            output_dir = "output"
            Path(output_dir).mkdir(exist_ok=True)
            file_path = os.path.join(output_dir, "srd_backend.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result["backend_srd"])
        
        return RegenerateSRDResponse(
            success=True,
            message=f"Successfully regenerated {request.srd_type} SRD with user feedback",
            frontend_srd=result.get("frontend_srd"),
            backend_srd=result.get("backend_srd")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error regenerating SRD: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)