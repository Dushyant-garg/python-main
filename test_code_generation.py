#!/usr/bin/env python3
"""
Test script for the backend code generation workflow
"""

import asyncio
import requests
import json

API_BASE_URL = "http://localhost:8000"

# Sample Backend SRD for testing
SAMPLE_BACKEND_SRD = """
# Backend Software Requirements Document

## 1. System Overview
This backend system provides REST API services for a task management application with user authentication, task CRUD operations, and team collaboration features.

## 2. Functional Requirements

### 2.1 User Management
- User registration and authentication
- JWT token-based authorization
- User profile management
- Password reset functionality

### 2.2 Task Management
- Create, read, update, delete tasks
- Task categorization and tagging
- Task assignment to users
- Task status tracking (pending, in-progress, completed)
- Due date management

### 2.3 Team Collaboration
- Create and manage teams
- Add/remove team members
- Team-based task visibility
- Task assignment within teams

## 3. Technical Requirements

### 3.1 Database Schema
- Users table (id, email, password_hash, created_at)
- Tasks table (id, title, description, status, due_date, user_id, team_id)
- Teams table (id, name, description, created_by)
- UserTeams junction table (user_id, team_id, role)

### 3.2 API Endpoints
- POST /auth/register - User registration
- POST /auth/login - User authentication
- GET /users/profile - Get user profile
- POST /tasks - Create new task
- GET /tasks - List tasks (with filtering)
- PUT /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task
- POST /teams - Create team
- GET /teams - List user's teams

### 3.3 Security Requirements
- Password hashing using bcrypt
- JWT token authentication
- Role-based access control
- Input validation and sanitization
- Rate limiting on authentication endpoints

### 3.4 Performance Requirements
- Response time < 200ms for CRUD operations
- Database indexing on frequently queried fields
- Connection pooling for database
- Async request handling

## 4. External Integrations
- Email service for notifications (SMTP)
- Optional: Slack integration for team notifications

## 5. Error Handling
- Comprehensive error responses with proper HTTP status codes
- Logging of all API requests and errors
- Graceful handling of database connection failures
"""

async def test_code_generation():
    """Test the backend code generation API"""
    print("🧪 Testing Backend Code Generation")
    print("=" * 50)
    
    try:
        # Test the code generation endpoint
        payload = {
            "backend_srd": SAMPLE_BACKEND_SRD,
            "project_name": "task_management_backend",
            "output_format": "files"
        }
        
        print("📤 Sending backend SRD for code generation...")
        print(f"📄 SRD Length: {len(SAMPLE_BACKEND_SRD)} characters")
        
        response = requests.post(f"{API_BASE_URL}/generate-backend-code", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['message']}")
            print(f"📁 Project Path: {result.get('project_path', 'N/A')}")
            print(f"📊 Files Generated: {result.get('file_count', 0)}")
            
            # Show generated files summary
            if result.get('generated_files'):
                print("\n📝 Generated Files:")
                for file_path in result['generated_files'].keys():
                    content_length = len(result['generated_files'][file_path])
                    print(f"  - {file_path} ({content_length} chars)")
                
                # Show a preview of one file
                first_file = list(result['generated_files'].keys())[0]
                preview = result['generated_files'][first_file][:300]
                print(f"\n👀 Preview of {first_file}:")
                print("-" * 40)
                print(preview + "..." if len(result['generated_files'][first_file]) > 300 else preview)
                print("-" * 40)
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
        print("💡 Run: python run_ui.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_api_health():
    """Test if the API is responsive"""
    print("\n🔍 Testing API Health...")
    
    try:
        health_response = requests.get(f"{API_BASE_URL}/")
        if health_response.status_code == 200:
            print("✅ API server is responsive")
            return True
        else:
            print(f"⚠️  API server responded with: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {str(e)}")
        return False

def test_agent_descriptions():
    """Show what each agent is responsible for"""
    print("\n🤖 Multi-Agent Code Generation System")
    print("=" * 50)
    
    agents = {
        "APIDesignerAgent": "Designs REST endpoints, HTTP methods, and request/response schemas",
        "ModelDeveloperAgent": "Creates database models, schemas, and relationships", 
        "BusinessLogicAgent": "Implements core business rules and service layer functions",
        "IntegrationAgent": "Handles external API integrations and third-party services",
        "DatabaseMigrationAgent": "Creates database setup scripts and migration files",
        "CodeCoordinatorAgent": "Orchestrates the process and ensures code integration"
    }
    
    for agent_name, description in agents.items():
        print(f"🎯 {agent_name}")
        print(f"   {description}")
        print()

if __name__ == "__main__":
    print("🚀 Starting Backend Code Generation Tests")
    
    # Show agent information
    test_agent_descriptions()
    
    # Test API health
    api_healthy = test_api_health()
    
    if api_healthy:
        print("\n" + "="*50)
        # Test the code generation workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            test_passed = loop.run_until_complete(test_code_generation())
        finally:
            loop.close()
        
        if test_passed:
            print("\n🎉 Code generation test completed successfully!")
            print("\n📋 Next Steps:")
            print("1. Start the application: python run_ui.py")
            print("2. Upload a document and generate SRDs")
            print("3. Use the 'Generate Backend Code' button")
            print("4. Review the generated files")
            print("5. Download the complete project")
        else:
            print("\n❌ Code generation test failed.")
    else:
        print("\n❌ API health check failed. Please start the server first.")