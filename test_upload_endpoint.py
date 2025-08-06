"""
Unit tests for /upload-document endpoint
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import tempfile
import shutil
from pathlib import Path

from app.main import app


class TestUploadDocument:
    """Test suite for upload document endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def temp_upload_dir(self):
        """Create temporary upload directory"""
        temp_dir = tempfile.mkdtemp()
        with patch('app.main.UPLOAD_DIR', temp_dir):
            yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def mock_parser(self):
        """Mock document parser"""
        with patch('app.main.document_parser') as mock:
            mock.parse_document = AsyncMock(return_value="Parsed content")
            yield mock
    
    def test_upload_txt_success(self, client, temp_upload_dir, mock_parser):
        """Test successful TXT file upload"""
        response = client.post(
            "/upload-document",
            files={"file": ("test.txt", b"Test content", "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "test.txt" in data["file_path"]
        assert data["parsed_text_preview"] == "Parsed content"
    
    def test_upload_pdf_success(self, client, temp_upload_dir, mock_parser):
        """Test successful PDF file upload"""
        response = client.post(
            "/upload-document",
            files={"file": ("doc.pdf", b"PDF content", "application/pdf")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "doc.pdf" in data["file_path"]
    
    def test_upload_docx_success(self, client, temp_upload_dir, mock_parser):
        """Test successful DOCX file upload"""
        response = client.post(
            "/upload-document",
            files={"file": ("doc.docx", b"DOCX content", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "doc.docx" in data["file_path"]
    
    def test_upload_unsupported_format(self, client):
        """Test upload with unsupported file format"""
        response = client.post(
            "/upload-document",
            files={"file": ("image.jpg", b"Image data", "image/jpeg")}
        )
        
        assert response.status_code == 400
        assert "Unsupported file format" in response.json()["detail"]
    
    def test_upload_no_file(self, client):
        """Test upload without file"""
        response = client.post("/upload-document")
        assert response.status_code == 422
    
    def test_upload_case_insensitive_extension(self, client, temp_upload_dir, mock_parser):
        """Test case insensitive file extensions"""
        response = client.post(
            "/upload-document",
            files={"file": ("test.TXT", b"Content", "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_preview_truncation(self, client, temp_upload_dir, mock_parser):
        """Test long content preview truncation"""
        long_content = "x" * 600  # Longer than 500 chars
        mock_parser.parse_document.return_value = long_content
        
        response = client.post(
            "/upload-document",
            files={"file": ("test.txt", b"Content", "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        preview = data["parsed_text_preview"]
        assert len(preview) <= 503  # 500 + "..."
        assert preview.endswith("...")
    
    def test_parser_exception(self, client, temp_upload_dir, mock_parser):
        """Test handling of parser exceptions"""
        mock_parser.parse_document.side_effect = Exception("Parser error")
        
        response = client.post(
            "/upload-document",
            files={"file": ("test.txt", b"Content", "text/plain")}
        )
        
        assert response.status_code == 500
        assert "Error uploading document" in response.json()["detail"]
    
    def test_empty_file(self, client, temp_upload_dir, mock_parser):
        """Test empty file upload"""
        mock_parser.parse_document.return_value = ""
        
        response = client.post(
            "/upload-document",
            files={"file": ("empty.txt", b"", "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["parsed_text_preview"] == ""
    
    def test_file_saved_correctly(self, client, temp_upload_dir, mock_parser):
        """Test that uploaded file is saved correctly"""
        file_content = b"Test file content"
        
        response = client.post(
            "/upload-document",
            files={"file": ("test.txt", file_content, "text/plain")}
        )
        
        assert response.status_code == 200
        
        # Check file was saved
        saved_file = Path(temp_upload_dir) / "test.txt"
        assert saved_file.exists()
        assert saved_file.read_bytes() == file_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])