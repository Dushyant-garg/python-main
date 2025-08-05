"""
Tests for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch, mock_open
import tempfile
import os
from pathlib import Path

from app.main import app


class TestAPIEndpoints:
    """Test suite for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.mark.api
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    @pytest.mark.api
    def test_upload_document_success(self, client):
        """Test successful document upload"""
        # Create a mock file
        test_file_content = b"Test document content for requirement analysis"
        
        with patch('app.main.document_parser') as mock_parser:
            mock_parser.parse_document.return_value = "Parsed content"
            
            response = client.post(
                "/upload-document",
                files={"file": ("test.txt", test_file_content, "text/plain")}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "file_path" in data
    
    @pytest.mark.api
    def test_upload_document_no_file(self, client):
        """Test document upload without file"""
        response = client.post("/upload-document")
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_analyze_requirements_success(self, client):
        """Test successful requirement analysis"""
        with patch('app.main.requirement_analyzer') as mock_analyzer:
            # Mock successful analysis
            mock_analyzer.analyze_requirements.return_value = {
                "frontend_srd": "# Frontend SRD\nTest content",
                "backend_srd": "# Backend SRD\nTest content",
                "analysis": "Analysis complete"
            }
            mock_analyzer.save_srds.return_value = ("frontend.md", "backend.md")
            
            response = client.post(
                "/analyze-requirements",
                json={"file_path": "test.txt", "output_directory": "output"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "frontend_srd_path" in data
            assert "backend_srd_path" in data
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_analyze_from_upload_success(self, client):
        """Test combined upload and analysis"""
        test_file_content = b"Project requirements document"
        
        with patch('app.main.document_parser') as mock_parser, \
             patch('app.main.requirement_analyzer') as mock_analyzer:
            
            mock_parser.parse_document.return_value = "Parsed requirements"
            mock_analyzer.analyze_requirements.return_value = {
                "frontend_srd": "Frontend requirements",
                "backend_srd": "Backend requirements",
                "analysis": "Complete analysis"
            }
            mock_analyzer.save_srds.return_value = ("frontend.md", "backend.md")
            
            response = client.post(
                "/analyze-from-upload",
                files={"file": ("requirements.txt", test_file_content, "text/plain")}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "analysis_summary" in data
    
    @pytest.mark.api
    def test_get_srd_content_frontend(self, client):
        """Test getting frontend SRD content"""
        mock_content = "# Frontend SRD\nTest content"
        
        with patch("builtins.open", mock_open(read_data=mock_content)), \
             patch("pathlib.Path.exists", return_value=True):
            
            response = client.get("/srd-content/frontend")
            
            assert response.status_code == 200
            data = response.json()
            assert data["content"] == mock_content
    
    @pytest.mark.api
    def test_get_srd_content_not_found(self, client):
        """Test getting SRD content when file doesn't exist"""
        with patch("pathlib.Path.exists", return_value=False):
            response = client.get("/srd-content/frontend")
            assert response.status_code == 404
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_regenerate_srd_success(self, client):
        """Test SRD regeneration with feedback"""
        with patch('app.main.requirement_analyzer') as mock_analyzer:
            mock_analyzer.regenerate_srd_with_feedback.return_value = {
                "frontend_srd": "# Improved Frontend SRD\nBetter content"
            }
            
            response = client.post(
                "/regenerate-srd",
                json={
                    "srd_type": "frontend",
                    "feedback": "Add more authentication details",
                    "original_analysis": "Basic analysis"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "frontend_srd" in data
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_generate_backend_code_success(self, client):
        """Test backend code generation"""
        with patch('app.main.backend_code_generator') as mock_generator:
            mock_generator.generate_backend_code.return_value = {
                "main.py": "FastAPI code",
                "models.py": "SQLAlchemy models"
            }
            mock_generator.save_generated_code.return_value = "generated_projects/test_backend"
            
            response = client.post(
                "/generate-backend-code",
                json={
                    "backend_srd": "# Backend SRD\nAPI requirements",
                    "project_name": "test_backend",
                    "output_format": "files"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["file_count"] == 2
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_generate_frontend_code_success(self, client):
        """Test frontend code generation"""
        with patch('app.main.frontend_code_generator') as mock_generator:
            mock_generator.generate_frontend_code.return_value = {
                "app.component.ts": "Angular component",
                "app.component.html": "Angular template"
            }
            mock_generator.save_generated_code.return_value = "generated_frontend_projects/test_frontend"
            
            response = client.post(
                "/generate-frontend-code",
                json={
                    "frontend_srd": "# Frontend SRD\nAngular requirements",
                    "project_name": "test_frontend",
                    "framework": "angular",
                    "output_format": "files"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["framework"] == "angular"
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_generate_fullstack_integration_success(self, client):
        """Test full-stack integration generation"""
        with patch('app.main.frontend_code_generator') as mock_frontend, \
             patch('app.main.backend_code_generator') as mock_backend, \
             patch('app.main.integration_coordinator') as mock_coordinator:
            
            # Mock frontend generation
            mock_frontend.generate_frontend_code.return_value = {
                "app.component.ts": "Angular component"
            }
            
            # Mock backend generation
            mock_backend.generate_backend_code.return_value = {
                "main.py": "FastAPI app"
            }
            
            # Mock integration
            mock_coordinator.generate_integration_package.return_value = {
                "project/frontend/app.component.ts": "Angular component",
                "project/backend/main.py": "FastAPI app",
                "project/docker-compose.yml": "Docker config"
            }
            mock_coordinator.save_integrated_package.return_value = "integrated_projects/test_fullstack"
            
            response = client.post(
                "/generate-fullstack-integration",
                json={
                    "frontend_srd": "# Frontend SRD\nAngular requirements",
                    "backend_srd": "# Backend SRD\nAPI requirements",
                    "project_name": "test_fullstack",
                    "include_docker": True,
                    "include_auth": True
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["frontend_file_count"] == 1
            assert data["backend_file_count"] == 1
            assert data["total_file_count"] == 3
    
    @pytest.mark.api
    def test_download_generated_code(self, client):
        """Test downloading generated code"""
        with patch("pathlib.Path.exists", return_value=True), \
             patch("shutil.make_archive") as mock_archive, \
             patch("fastapi.responses.FileResponse") as mock_response:
            
            mock_archive.return_value = "test.zip"
            mock_response.return_value = Mock()
            
            response = client.get("/download-generated-code/test_project")
            
            # Should attempt to create zip
            mock_archive.assert_called_once()
    
    @pytest.mark.api
    def test_error_handling_empty_srd(self, client):
        """Test error handling for empty SRD"""
        response = client.post(
            "/generate-backend-code",
            json={
                "backend_srd": "",
                "project_name": "test"
            }
        )
        
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    @pytest.mark.api
    def test_error_handling_invalid_srd_type(self, client):
        """Test error handling for invalid SRD type"""
        response = client.post(
            "/regenerate-srd",
            json={
                "srd_type": "invalid",
                "feedback": "test feedback"
            }
        )
        
        assert response.status_code == 400
        assert "must be 'frontend' or 'backend'" in response.json()["detail"]


class TestAPIErrorHandling:
    """Test API error handling scenarios"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.mark.api
    def test_file_upload_size_limit(self, client):
        """Test file upload size handling"""
        # Create a large file (mock)
        large_content = b"x" * (10 * 1024 * 1024)  # 10MB
        
        response = client.post(
            "/upload-document",
            files={"file": ("large.txt", large_content, "text/plain")}
        )
        
        # Should handle large files gracefully
        assert response.status_code in [200, 413]  # Success or Request Entity Too Large
    
    @pytest.mark.asyncio
    @pytest.mark.api
    async def test_analysis_timeout_handling(self, client):
        """Test handling of analysis timeouts"""
        with patch('app.main.requirement_analyzer') as mock_analyzer:
            mock_analyzer.analyze_requirements.side_effect = asyncio.TimeoutError("Analysis timeout")
            
            response = client.post(
                "/analyze-requirements",
                json={"file_path": "test.txt"}
            )
            
            assert response.status_code == 500
    
    @pytest.mark.api
    def test_invalid_file_type(self, client):
        """Test handling of invalid file types"""
        invalid_content = b"Not a valid document"
        
        with patch('app.main.document_parser') as mock_parser:
            mock_parser.parse_document.side_effect = ValueError("Unsupported file type")
            
            response = client.post(
                "/upload-document",
                files={"file": ("invalid.exe", invalid_content, "application/octet-stream")}
            )
            
            assert response.status_code == 500
    
    @pytest.mark.api
    def test_missing_output_directory(self, client):
        """Test handling when output directory doesn't exist"""
        with patch("pathlib.Path.exists", return_value=False):
            response = client.get("/srd-content/frontend?output_dir=nonexistent")
            assert response.status_code == 404


class TestAPIValidation:
    """Test API input validation"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.mark.api
    def test_required_fields_validation(self, client):
        """Test validation of required fields"""
        # Missing backend_srd
        response = client.post(
            "/generate-backend-code",
            json={"project_name": "test"}
        )
        assert response.status_code == 422
        
        # Missing frontend_srd for fullstack
        response = client.post(
            "/generate-fullstack-integration",
            json={"backend_srd": "test"}
        )
        assert response.status_code == 422
    
    @pytest.mark.api
    def test_optional_fields_defaults(self, client):
        """Test default values for optional fields"""
        with patch('app.main.backend_code_generator') as mock_generator:
            mock_generator.generate_backend_code.return_value = {"test.py": "code"}
            mock_generator.save_generated_code.return_value = "test_path"
            
            response = client.post(
                "/generate-backend-code",
                json={"backend_srd": "# Test SRD"}
            )
            
            assert response.status_code == 200
            # Should use default project name
            mock_generator.generate_backend_code.assert_called_with(
                backend_srd="# Test SRD",
                project_name="generated_backend"
            )
    
    @pytest.mark.api
    def test_enum_validation(self, client):
        """Test enumeration field validation"""
        response = client.post(
            "/generate-frontend-code",
            json={
                "frontend_srd": "# Test SRD",
                "framework": "react"  # Should be "angular"
            }
        )
        
        assert response.status_code == 400
        assert "only Angular framework is supported" in response.json()["detail"]


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.mark.slow
    def test_complete_workflow_simulation(self, client):
        """Test complete workflow from upload to code generation"""
        # This test simulates the complete workflow but with mocked agents
        # to avoid actual AI calls during testing
        
        test_file_content = b"Project Requirements: Build a task management system"
        
        with patch('app.main.document_parser') as mock_parser, \
             patch('app.main.requirement_analyzer') as mock_analyzer, \
             patch('app.main.backend_code_generator') as mock_backend, \
             patch('app.main.frontend_code_generator') as mock_frontend:
            
            # Setup mocks
            mock_parser.parse_document.return_value = "Parsed requirements"
            mock_analyzer.analyze_requirements.return_value = {
                "frontend_srd": "# Frontend SRD\nUI requirements",
                "backend_srd": "# Backend SRD\nAPI requirements",
                "analysis": "Complete analysis"
            }
            mock_analyzer.save_srds.return_value = ("frontend.md", "backend.md")
            
            mock_backend.generate_backend_code.return_value = {"main.py": "FastAPI code"}
            mock_backend.save_generated_code.return_value = "backend_path"
            
            mock_frontend.generate_frontend_code.return_value = {"app.component.ts": "Angular code"}
            mock_frontend.save_generated_code.return_value = "frontend_path"
            
            # Step 1: Upload and analyze
            response1 = client.post(
                "/analyze-from-upload",
                files={"file": ("requirements.txt", test_file_content, "text/plain")}
            )
            assert response1.status_code == 200
            
            # Step 2: Generate backend code
            response2 = client.post(
                "/generate-backend-code",
                json={
                    "backend_srd": "# Backend SRD\nAPI requirements",
                    "project_name": "test_backend"
                }
            )
            assert response2.status_code == 200
            
            # Step 3: Generate frontend code
            response3 = client.post(
                "/generate-frontend-code",
                json={
                    "frontend_srd": "# Frontend SRD\nUI requirements",
                    "project_name": "test_frontend"
                }
            )
            assert response3.status_code == 200
            
            # Verify all steps completed successfully
            assert all(r.json()["success"] for r in [response1, response2, response3])