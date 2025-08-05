from pydantic import BaseModel
from typing import Optional, Dict

class DocumentAnalysisRequest(BaseModel):
    """Request model for document analysis"""
    file_path: str
    output_directory: Optional[str] = "output"

class DocumentAnalysisResponse(BaseModel):
    """Response model for document analysis"""
    success: bool
    message: str
    frontend_srd_path: Optional[str] = None
    backend_srd_path: Optional[str] = None
    analysis_summary: Optional[str] = None

class SRDContent(BaseModel):
    """Model for SRD content"""
    frontend_srd: str
    backend_srd: str
    analysis: str

class UploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool
    message: str
    file_path: Optional[str] = None
    parsed_text_preview: Optional[str] = None

class RegenerateSRDRequest(BaseModel):
    """Request model for SRD regeneration with feedback"""
    srd_type: str  # "frontend" or "backend"
    feedback: str
    original_analysis: Optional[str] = None

class RegenerateSRDResponse(BaseModel):
    """Response model for SRD regeneration"""
    success: bool
    message: str
    frontend_srd: Optional[str] = None
    backend_srd: Optional[str] = None

class CodeGenerationRequest(BaseModel):
    """Request model for backend code generation"""
    backend_srd: str
    project_name: Optional[str] = "generated_backend"
    output_format: Optional[str] = "files"  # "files" or "zip"

class CodeGenerationResponse(BaseModel):
    """Response model for backend code generation"""
    success: bool
    message: str
    project_path: Optional[str] = None
    generated_files: Optional[Dict[str, str]] = None
    file_count: Optional[int] = None

class FrontendCodeGenerationRequest(BaseModel):
    """Request model for frontend code generation"""
    frontend_srd: str
    project_name: Optional[str] = "generated_frontend"
    framework: Optional[str] = "angular"  # Currently supports "angular"
    output_format: Optional[str] = "files"  # "files" or "zip"

class FrontendCodeGenerationResponse(BaseModel):
    """Response model for frontend code generation"""
    success: bool
    message: str
    project_path: Optional[str] = None
    generated_files: Optional[Dict[str, str]] = None
    file_count: Optional[int] = None
    framework: Optional[str] = None