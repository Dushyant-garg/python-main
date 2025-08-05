"""
Pytest configuration and shared fixtures for agent testing
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any
import os
import tempfile
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing"""
    mock_client = Mock()
    mock_client.chat = Mock()
    mock_client.chat.completions = Mock()
    mock_client.chat.completions.create = AsyncMock()
    
    # Default response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Mock response content"
    
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_autogen_message():
    """Mock AutoGen message object"""
    mock_message = Mock()
    mock_message.content = "Test message content"
    mock_message.source = "TestAgent"
    return mock_message


@pytest.fixture
def mock_autogen_result():
    """Mock AutoGen conversation result"""
    mock_result = Mock()
    mock_result.messages = []
    return mock_result


@pytest.fixture
def sample_frontend_srd():
    """Sample frontend SRD for testing"""
    return """
# Frontend Software Requirements Document

## 1. System Overview
Angular-based web application for task management with user authentication and real-time updates.

## 2. Core Components

### 2.1 Authentication Module
- Login/Register forms with validation
- JWT token management
- Protected route guards
- Password reset functionality

### 2.2 Task Management
- Task list with filtering and sorting
- Task creation and editing forms
- Drag-and-drop status updates
- Due date management

### 2.3 Dashboard
- Task overview widgets
- Progress charts
- Recent activity feed
- Quick actions panel

## 3. Technical Requirements
- Angular 16+ with TypeScript
- Angular Material for UI components
- NgRx for state management
- Reactive forms for user input
- HTTP interceptors for API calls
"""


@pytest.fixture
def sample_backend_srd():
    """Sample backend SRD for testing"""
    return """
# Backend Software Requirements Document

## 1. System Overview
FastAPI-based REST API for task management with user authentication and data persistence.

## 2. Core Functionality

### 2.1 User Management
- User registration and authentication
- JWT token generation and validation
- User profile management
- Password reset with email verification

### 2.2 Task Operations
- CRUD operations for tasks
- Task assignment and status tracking
- Due date management and notifications
- Task filtering and search

### 2.3 Data Management
- PostgreSQL database integration
- SQLAlchemy ORM models
- Alembic database migrations
- Data validation with Pydantic

## 3. Technical Specifications
- FastAPI with async/await support
- JWT authentication with refresh tokens
- CORS configuration for frontend
- Comprehensive error handling
- API documentation with OpenAPI
"""


@pytest.fixture
def sample_document_text():
    """Sample document text for requirement analysis"""
    return """
Project Requirements: Task Management System

Overview:
We need to build a comprehensive task management system that allows users to create, manage, and track tasks. The system should support team collaboration and real-time updates.

Frontend Requirements:
- Modern web interface built with Angular
- User-friendly dashboard with task overview
- Responsive design for mobile and desktop
- Real-time notifications and updates
- User authentication and authorization

Backend Requirements:
- RESTful API built with FastAPI
- User management with JWT authentication
- Task CRUD operations with database persistence
- Email notifications for task updates
- Role-based access control for teams

Technical Stack:
- Frontend: Angular, TypeScript, Angular Material
- Backend: FastAPI, Python, PostgreSQL
- Authentication: JWT tokens
- Real-time: WebSocket connections
- Deployment: Docker containers
"""


@pytest.fixture
def temp_output_dir():
    """Temporary directory for test file outputs"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_file_system():
    """Mock file system operations"""
    with patch('pathlib.Path.mkdir'), \
         patch('builtins.open', create=True), \
         patch('pathlib.Path.exists', return_value=True):
        yield


@pytest.fixture
def mock_agent_conversation():
    """Mock agent conversation with sample messages"""
    messages = []
    
    # Mock analyst message
    analyst_msg = Mock()
    analyst_msg.content = """
    ANALYSIS COMPLETE:
    - Frontend requirements identified: Authentication, Dashboard, Task Management
    - Backend requirements identified: API, Database, Authentication
    - Integration points: JWT auth, REST API consumption
    """
    analyst_msg.source = "RequirementAnalyst"
    messages.append(analyst_msg)
    
    # Mock frontend specialist message
    frontend_msg = Mock()
    frontend_msg.content = """
    # Frontend Software Requirements Document
    ## Authentication Module
    - Login/Register components
    - Route guards for protected areas
    ## Task Management
    - Task list and creation forms
    - Real-time updates with WebSocket
    """
    frontend_msg.source = "FrontendSpecialist"
    messages.append(frontend_msg)
    
    # Mock backend specialist message
    backend_msg = Mock()
    backend_msg.content = """
    # Backend Software Requirements Document
    ## User Management
    - JWT authentication endpoints
    - User registration and login
    ## Task API
    - CRUD operations for tasks
    - Database models with SQLAlchemy
    """
    backend_msg.source = "BackendSpecialist"
    messages.append(backend_msg)
    
    return messages


@pytest.fixture
def mock_generated_code():
    """Mock generated code files"""
    return {
        "app.component.ts": """
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Test App';
}
""",
        "app.component.html": """
<div class="app-container">
  <h1>{{title}}</h1>
  <router-outlet></router-outlet>
</div>
""",
        "main.py": """
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "Hello World"}
""",
        "requirements.txt": """
fastapi==0.116.1
uvicorn==0.32.1
"""
    }


@pytest.fixture
def environment_vars():
    """Set up environment variables for testing"""
    test_vars = {
        'OPENAI_API_KEY': 'test-api-key',
        'OPENAI_MODEL': 'gpt-4',
        'DATABASE_URL': 'sqlite:///test.db'
    }
    
    # Store original values
    original_vars = {}
    for key, value in test_vars.items():
        original_vars[key] = os.environ.get(key)
        os.environ[key] = value
    
    yield test_vars
    
    # Restore original values
    for key, original_value in original_vars.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def mock_autogen_team():
    """Mock AutoGen team/group chat"""
    mock_team = AsyncMock()
    mock_team.run = AsyncMock()
    
    # Create mock result
    mock_result = Mock()
    mock_result.messages = []
    mock_team.run.return_value = mock_result
    
    return mock_team


class AgentTestHelper:
    """Helper class for agent testing utilities"""
    
    @staticmethod
    def create_mock_message(content: str, source: str = "TestAgent"):
        """Create a mock message object"""
        msg = Mock()
        msg.content = content
        msg.source = source
        return msg
    
    @staticmethod
    def create_mock_result(messages: List):
        """Create a mock conversation result"""
        result = Mock()
        result.messages = messages
        return result
    
    @staticmethod
    def assert_file_generated(generated_files: Dict[str, str], filename: str):
        """Assert that a specific file was generated"""
        assert any(filename in path for path in generated_files.keys()), \
            f"Expected file '{filename}' not found in generated files: {list(generated_files.keys())}"
    
    @staticmethod
    def assert_content_contains(content: str, expected_text: str):
        """Assert that content contains expected text"""
        assert expected_text in content, \
            f"Expected text '{expected_text}' not found in content"


@pytest.fixture
def agent_test_helper():
    """Provide agent testing helper utilities"""
    return AgentTestHelper


# Async test decorators
pytest_plugins = ('pytest_asyncio',)