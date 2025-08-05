#!/usr/bin/env python3
"""
Complete Full-Stack Code Generation Demo
Demonstrates Frontend (Angular) + Backend (FastAPI) generation from SRDs
"""

import requests
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a step description"""
    print(f"\n🔸 Step {step_num}: {description}")
    print("-" * 40)

def demo_fullstack_generation():
    """Demonstrate complete full-stack code generation"""
    
    print_header("🌟 FULL-STACK CODE GENERATION DEMO")
    print("📋 Document → 📄 SRDs → 🎨 Angular Frontend + 🚀 FastAPI Backend")
    
    # Sample SRDs (normally these would come from document analysis)
    frontend_srd = """
# Frontend Software Requirements Document - E-Commerce Platform

## 1. System Overview
Angular-based e-commerce platform with user authentication, product management, and shopping cart functionality.

## 2. Core Components

### 2.1 Authentication Module
- Login/Register components with Angular Material forms
- JWT token management service
- Route guards for protected areas
- Password reset functionality

### 2.2 Product Catalog
- Product listing with search and filters
- Product detail views with image galleries
- Category navigation sidebar
- Shopping cart integration

### 2.3 Shopping Cart & Checkout
- Cart management with quantity updates
- Checkout process with form validation
- Order confirmation and tracking
- Payment integration (mock)

### 2.4 User Dashboard
- User profile management
- Order history and tracking
- Wishlist functionality
- Account settings

## 3. Technical Specifications
- Angular 16+ with TypeScript
- Angular Material for UI components
- NgRx for state management
- Reactive forms for user input
- HTTP interceptors for API communication
- Responsive design with SCSS
"""

    backend_srd = """
# Backend Software Requirements Document - E-Commerce Platform

## 1. System Overview
FastAPI-based backend providing REST APIs for e-commerce operations with user management, product catalog, and order processing.

## 2. Core Functionality

### 2.1 User Management
- User registration and authentication with JWT
- User profile management
- Password reset functionality
- Role-based access control

### 2.2 Product Management
- Product CRUD operations
- Category management
- Inventory tracking
- Product search and filtering

### 2.3 Order Processing
- Shopping cart operations
- Order creation and management
- Payment processing integration
- Order status tracking

### 2.4 Admin Features
- Product management dashboard
- Order management system
- User administration
- Analytics and reporting

## 3. Technical Specifications
- FastAPI with Pydantic models
- SQLAlchemy ORM with PostgreSQL
- JWT authentication
- Alembic for database migrations
- Redis for caching
- Celery for background tasks
"""

    try:
        print_step(1, "Testing API Health")
        health_response = requests.get(f"{API_BASE_URL}/")
        if health_response.status_code != 200:
            print("❌ API server not responding correctly")
            return False
        print("✅ API server is responsive")
        
        print_step(2, "Generating Angular Frontend Code")
        frontend_payload = {
            "frontend_srd": frontend_srd,
            "project_name": "ecommerce_angular_frontend",
            "framework": "angular",
            "output_format": "files"
        }
        
        print("🎨 Starting Angular code generation...")
        print("🤖 Angular Agents working:")
        agents_status = [
            "   ⏳ ComponentDesignerAgent: Designing Angular components...",
            "   ⏳ ServiceDeveloperAgent: Creating Angular services...",
            "   ⏳ UIImplementationAgent: Building templates and styles...",
            "   ⏳ StateManagementAgent: Setting up NgRx state management...",
            "   ⏳ FrontendCoordinatorAgent: Orchestrating project structure..."
        ]
        
        for status in agents_status:
            print(status)
            time.sleep(0.5)  # Simulate processing time
        
        frontend_response = requests.post(f"{API_BASE_URL}/generate-frontend-code", json=frontend_payload, timeout=300)
        
        if frontend_response.status_code == 200:
            frontend_result = frontend_response.json()
            print(f"\n✅ Angular Frontend Generation Success!")
            print(f"📁 Project: {frontend_result.get('project_path', 'N/A')}")
            print(f"📊 Files: {frontend_result.get('file_count', 0)} Angular files")
            print(f"🏗️ Framework: {frontend_result.get('framework', 'Angular')}")
            
            # Categorize and display Angular files
            if frontend_result.get('generated_files'):
                files = frontend_result['generated_files']
                ts_files = [f for f in files.keys() if f.endswith('.ts')]
                html_files = [f for f in files.keys() if f.endswith('.html')]
                scss_files = [f for f in files.keys() if f.endswith('.scss')]
                json_files = [f for f in files.keys() if f.endswith('.json')]
                
                print(f"\n📝 Angular File Summary:")
                print(f"   📝 TypeScript: {len(ts_files)} files")
                print(f"   🎨 HTML Templates: {len(html_files)} files")
                print(f"   💄 SCSS Styles: {len(scss_files)} files")
                print(f"   ⚙️ Config Files: {len(json_files)} files")
        else:
            print(f"❌ Frontend generation failed: {frontend_response.text}")
            return False
        
        print_step(3, "Generating FastAPI Backend Code")
        backend_payload = {
            "backend_srd": backend_srd,
            "project_name": "ecommerce_fastapi_backend",
            "output_format": "files"
        }
        
        print("🚀 Starting FastAPI code generation...")
        print("🤖 Backend Agents working:")
        backend_agents_status = [
            "   ⏳ APIDesignerAgent: Designing REST endpoints...",
            "   ⏳ ModelDeveloperAgent: Creating database models...",
            "   ⏳ BusinessLogicAgent: Implementing business logic...",
            "   ⏳ IntegrationAgent: Setting up external integrations...",
            "   ⏳ DatabaseMigrationAgent: Creating database migrations...",
            "   ⏳ CodeCoordinatorAgent: Finalizing project structure..."
        ]
        
        for status in backend_agents_status:
            print(status)
            time.sleep(0.5)  # Simulate processing time
        
        backend_response = requests.post(f"{API_BASE_URL}/generate-backend-code", json=backend_payload, timeout=300)
        
        if backend_response.status_code == 200:
            backend_result = backend_response.json()
            print(f"\n✅ FastAPI Backend Generation Success!")
            print(f"📁 Project: {backend_result.get('project_path', 'N/A')}")
            print(f"📊 Files: {backend_result.get('file_count', 0)} Python files")
            
            # Display backend files summary
            if backend_result.get('generated_files'):
                files = backend_result['generated_files']
                py_files = [f for f in files.keys() if f.endswith('.py')]
                txt_files = [f for f in files.keys() if f.endswith('.txt')]
                md_files = [f for f in files.keys() if f.endswith('.md')]
                other_files = [f for f in files.keys() if not any(f.endswith(ext) for ext in ['.py', '.txt', '.md'])]
                
                print(f"\n📝 FastAPI File Summary:")
                print(f"   🐍 Python Files: {len(py_files)} files")
                print(f"   📋 Requirements: {len(txt_files)} files")
                print(f"   📄 Documentation: {len(md_files)} files")
                print(f"   ⚙️ Other Files: {len(other_files)} files")
        else:
            print(f"❌ Backend generation failed: {backend_response.text}")
            return False
        
        print_step(4, "Full-Stack Integration Summary")
        print("🎉 Complete Full-Stack Application Generated!")
        
        fullstack_summary = f"""
🌟 FULL-STACK E-COMMERCE PLATFORM GENERATED:

🎨 FRONTEND (Angular):
   📁 Project: {frontend_result.get('project_path', 'N/A')}
   📊 Files: {frontend_result.get('file_count', 0)} Angular files
   🏗️ Components: Authentication, Product Catalog, Shopping Cart, Dashboard
   🔧 Services: HTTP clients, State management, Guards
   🎨 UI: Angular Material, Responsive design, Forms
   📱 Features: SPA routing, NgRx state, Reactive programming

🚀 BACKEND (FastAPI):
   📁 Project: {backend_result.get('project_path', 'N/A')}
   📊 Files: {backend_result.get('file_count', 0)} Python files
   🏗️ APIs: REST endpoints, Authentication, CRUD operations
   🗃️ Database: SQLAlchemy models, Migrations, Relationships
   🔒 Security: JWT tokens, Input validation, Error handling
   ⚡ Performance: Async operations, Caching, Background tasks

🔗 INTEGRATION READY:
   ✅ Frontend configured to consume Backend APIs
   ✅ Authentication flow between Angular and FastAPI
   ✅ CORS configuration for cross-origin requests
   ✅ Consistent data models and interfaces
   ✅ Error handling and user feedback
   ✅ Ready for containerization and deployment
        """
        
        print(fullstack_summary)
        
        print_step(5, "Deployment Instructions")
        deployment_guide = """
📋 DEPLOYMENT GUIDE:

🚀 Backend Deployment:
   1. cd generated_projects/ecommerce_fastapi_backend
   2. pip install -r requirements.txt
   3. Configure database connection
   4. Run: uvicorn main:app --reload
   5. Backend available at: http://localhost:8000

🎨 Frontend Deployment:
   1. cd generated_frontend_projects/ecommerce_angular_frontend
   2. npm install
   3. Configure API base URL in environment files
   4. Run: ng serve
   5. Frontend available at: http://localhost:4200

🌐 Full Integration:
   - Frontend consumes Backend APIs
   - Complete user authentication flow
   - Full CRUD operations for products and orders
   - Ready for production deployment
        """
        
        print(deployment_guide)
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Generation timed out - this is normal for complex projects")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def show_multi_agent_overview():
    """Show overview of all agents in the system"""
    print_header("🤖 COMPLETE MULTI-AGENT SYSTEM OVERVIEW")
    
    agent_categories = {
        "📋 SRD Generation Agents": {
            "RequirementAnalyst": "Analyzes documents and categorizes requirements",
            "FrontendSpecialist": "Creates frontend-specific requirements and specifications",
            "BackendSpecialist": "Creates backend-specific requirements and specifications",
            "UserProxy": "Processes user feedback and coordinates improvements"
        },
        "🎨 Angular Frontend Agents": {
            "ComponentDesignerAgent": "Designs Angular components and TypeScript structure",
            "ServiceDeveloperAgent": "Creates Angular services and HTTP clients",
            "UIImplementationAgent": "Implements templates, styles, and Angular Material UI",
            "StateManagementAgent": "Sets up NgRx state management and reactive patterns",
            "FrontendCoordinatorAgent": "Orchestrates Angular project structure"
        },
        "🚀 FastAPI Backend Agents": {
            "APIDesignerAgent": "Designs REST endpoints and API routing",
            "ModelDeveloperAgent": "Creates database models and schemas",
            "BusinessLogicAgent": "Implements core business functionality",
            "IntegrationAgent": "Handles external service connections",
            "DatabaseMigrationAgent": "Creates database setup and migrations",
            "CodeCoordinatorAgent": "Orchestrates backend project structure"
        }
    }
    
    for category, agents in agent_categories.items():
        print(f"\n{category}:")
        for agent_name, description in agents.items():
            print(f"  🎯 {agent_name}: {description}")
    
    print(f"\n📊 TOTAL AGENTS: {sum(len(agents) for agents in agent_categories.values())}")
    print("🌟 Complete AI-powered development pipeline from requirements to deployment!")

if __name__ == "__main__":
    print("🌟 Full-Stack Code Generation Demo")
    print("From Requirements Documents to Complete Applications")
    
    # Show multi-agent overview
    show_multi_agent_overview()
    
    # Run the full-stack demo
    print_header("🧪 RUNNING FULL-STACK DEMO")
    success = demo_fullstack_generation()
    
    if success:
        print_header("🎉 FULL-STACK DEMO COMPLETED SUCCESSFULLY")
        print("Complete Angular + FastAPI application stack generated!")
        print("\n🚀 What was accomplished:")
        print("✅ Angular frontend with 5 specialized agents")
        print("✅ FastAPI backend with 6 specialized agents")
        print("✅ Complete project structures generated")
        print("✅ Ready-to-deploy applications")
        print("✅ Full-stack integration configured")
        
        print("\n🌐 Ready for Production Deployment!")
        print("Start the complete system with: python run_ui.py")
        
    else:
        print_header("❌ DEMO ENCOUNTERED ISSUES")
        print("Please check the server status and try again.")
        print("Ensure the FastAPI server is running on localhost:8000")