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