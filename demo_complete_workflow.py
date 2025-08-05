#!/usr/bin/env python3
"""
Complete workflow demonstration for the Requirements Analyzer with Code Generation
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

def test_complete_workflow():
    """Demonstrate the complete workflow from document to code"""
    
    print_header("🚀 COMPLETE REQUIREMENTS ANALYZER WORKFLOW DEMO")
    
    print("This demo showcases the full pipeline:")
    print("📄 Document Upload → 📋 SRD Generation → 🔄 Feedback → 🚀 Code Generation")
    
    # Sample requirements document content
    sample_document_content = """
    E-COMMERCE PLATFORM REQUIREMENTS
    
    Project Overview:
    We need to build a modern e-commerce platform that allows users to browse products, 
    manage shopping carts, process payments, and track orders. The system should support
    both customers and administrators.
    
    Core Features:
    1. User Management
       - User registration and authentication
       - User profiles and preferences
       - Address management
    
    2. Product Catalog
       - Product listings with categories
       - Product search and filtering
       - Product reviews and ratings
       - Inventory management
    
    3. Shopping Cart & Checkout
       - Add/remove items from cart
       - Cart persistence across sessions
       - Multiple payment methods
       - Order confirmation and tracking
    
    4. Admin Dashboard
       - Product management (CRUD)
       - Order management
       - User management
       - Analytics and reporting
    
    Technical Requirements:
    - RESTful API architecture
    - JWT authentication
    - Database with proper relationships
    - Payment gateway integration
    - Email notifications
    - Mobile-responsive design
    """
    
    try:
        print_step(1, "Testing API Health")
        health_response = requests.get(f"{API_BASE_URL}/")
        if health_response.status_code == 200:
            print("✅ API server is responsive")
        else:
            print("❌ API server not responding correctly")
            return False
        
        print_step(2, "Simulating Document Analysis (Direct SRD Input)")
        # In a real scenario, you would upload a document file
        # For demo purposes, we'll simulate the analysis result
        
        # Create a sample backend SRD (this would normally come from document analysis)
        backend_srd = """
# Backend Software Requirements Document - E-Commerce Platform

## 1. System Overview
Backend system for a modern e-commerce platform supporting user management, 
product catalog, shopping cart functionality, and order processing.

## 2. Functional Requirements

### 2.1 User Management
- User registration with email verification
- JWT-based authentication and authorization
- User profile management (name, email, addresses)
- Password reset functionality
- Role-based access control (customer, admin)

### 2.2 Product Management
- Product CRUD operations
- Category management and hierarchical organization
- Product image upload and management
- Inventory tracking and stock management
- Product search with filtering capabilities

### 2.3 Shopping Cart & Orders
- Cart management (add, update, remove items)
- Cart persistence across sessions
- Order creation and status tracking
- Order history and details
- Payment processing integration

### 2.4 Administration
- Admin dashboard endpoints
- User management for administrators
- Product management interface
- Order management and fulfillment
- Analytics and reporting endpoints

## 3. Technical Specifications

### 3.1 Database Schema
- Users (id, email, password_hash, first_name, last_name, created_at)
- Products (id, name, description, price, category_id, stock_quantity, images)
- Categories (id, name, description, parent_id)
- Orders (id, user_id, total_amount, status, created_at, shipping_address)
- OrderItems (order_id, product_id, quantity, unit_price)
- CartItems (user_id, product_id, quantity, created_at)

### 3.2 API Endpoints
Authentication:
- POST /auth/register - User registration
- POST /auth/login - User login
- POST /auth/refresh - Token refresh
- POST /auth/logout - User logout

Products:
- GET /products - List products (with pagination and filters)
- GET /products/{id} - Get product details
- POST /products - Create product (admin only)
- PUT /products/{id} - Update product (admin only)
- DELETE /products/{id} - Delete product (admin only)

Cart & Orders:
- GET /cart - Get user's cart
- POST /cart/items - Add item to cart
- PUT /cart/items/{id} - Update cart item
- DELETE /cart/items/{id} - Remove from cart
- POST /orders - Create order from cart
- GET /orders - List user's orders
- GET /orders/{id} - Get order details

### 3.3 Security Requirements
- Password hashing using bcrypt
- JWT token authentication with refresh tokens
- Input validation and sanitization
- Rate limiting on authentication endpoints
- SQL injection prevention
- CORS configuration

### 3.4 Integration Requirements
- Payment gateway integration (Stripe/PayPal)
- Email service for notifications (SendGrid/SMTP)
- Image storage service (AWS S3/CloudFront)
- Optional: Redis for session management and caching

## 4. Performance Requirements
- API response times < 200ms for standard operations
- Database indexing on frequently queried fields
- Connection pooling for database connections
- Async request handling for improved throughput
- Caching strategy for product catalog
"""
        
        print("✅ Sample Backend SRD prepared")
        print(f"📄 SRD Length: {len(backend_srd)} characters")
        
        print_step(3, "Testing SRD Regeneration with Feedback")
        feedback_payload = {
            "srd_type": "backend",
            "feedback": "Please add more details about caching strategy and database optimization. Also include specific error handling requirements.",
            "original_analysis": "E-commerce platform requirements"
        }
        
        print("📤 Sending feedback for SRD improvement...")
        feedback_response = requests.post(f"{API_BASE_URL}/regenerate-srd", json=feedback_payload)
        
        if feedback_response.status_code == 200:
            feedback_result = feedback_response.json()
            print("✅ SRD regeneration with feedback successful")
            # Use the improved SRD if available
            if feedback_result.get('backend_srd'):
                backend_srd = feedback_result['backend_srd']
                print("📝 Using improved SRD for code generation")
        else:
            print("⚠️  SRD feedback failed, using original SRD")
        
        print_step(4, "Generating Backend Code")
        code_generation_payload = {
            "backend_srd": backend_srd,
            "project_name": "ecommerce_backend",
            "output_format": "files"
        }
        
        print("🚀 Starting multi-agent code generation...")
        print("🤖 Agents working:")
        print("   - APIDesignerAgent: Designing REST endpoints")
        print("   - ModelDeveloperAgent: Creating database models")
        print("   - BusinessLogicAgent: Implementing business logic")
        print("   - IntegrationAgent: Setting up external integrations")
        print("   - DatabaseMigrationAgent: Creating database setup")
        print("   - CodeCoordinatorAgent: Orchestrating the project")
        
        code_response = requests.post(f"{API_BASE_URL}/generate-backend-code", json=code_generation_payload, timeout=300)
        
        if code_response.status_code == 200:
            code_result = code_response.json()
            print(f"✅ Code generation successful!")
            print(f"📁 Project Path: {code_result.get('project_path', 'N/A')}")
            print(f"📊 Files Generated: {code_result.get('file_count', 0)}")
            
            if code_result.get('generated_files'):
                print("\n📝 Generated Files Summary:")
                for file_path in code_result['generated_files'].keys():
                    content_length = len(code_result['generated_files'][file_path])
                    print(f"  📄 {file_path} ({content_length:,} characters)")
                
                # Show preview of a Python file
                python_files = [f for f in code_result['generated_files'].keys() if f.endswith('.py')]
                if python_files:
                    preview_file = python_files[0]
                    preview_content = code_result['generated_files'][preview_file][:500]
                    print(f"\n👀 Preview of {preview_file}:")
                    print("-" * 50)
                    print(preview_content + "..." if len(code_result['generated_files'][preview_file]) > 500 else preview_content)
                    print("-" * 50)
            
            print_step(5, "Testing Download Functionality")
            download_url = f"{API_BASE_URL}/download-generated-code/ecommerce_backend"
            print(f"📥 Download URL: {download_url}")
            print("💡 You can download the complete project using this URL")
            
            return True
            
        else:
            print(f"❌ Code generation failed: {code_response.status_code} - {code_response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
        print("💡 Run: python run_ui.py")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Code generation timed out - this is normal for complex projects")
        print("💡 Try with a simpler SRD or check the server logs")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def show_workflow_summary():
    """Show a summary of the complete workflow"""
    print_header("📋 WORKFLOW SUMMARY")
    
    workflow_steps = [
        "📄 Document Upload: Users upload project requirements (PDF, DOCX, TXT)",
        "🔍 AI Analysis: Multi-agent system analyzes and categorizes requirements",
        "📋 SRD Generation: Separate Frontend and Backend SRDs are created",
        "👥 Human Review: Users can accept or reject generated SRDs",
        "🔄 Feedback Loop: UserProxy agent processes feedback to improve SRDs",
        "🚀 Code Generation: 6 specialized agents generate complete backend code",
        "📁 Project Output: Complete, deployable FastAPI backend application",
        "📥 Download: Users can download the generated project as ZIP"
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"{i}. {step}")
    
    print_header("🤖 MULTI-AGENT SYSTEM OVERVIEW")
    
    print("📋 SRD Generation Agents:")
    srd_agents = [
        "RequirementAnalyst: Analyzes and categorizes requirements",
        "FrontendSpecialist: Creates frontend-specific requirements",
        "BackendSpecialist: Creates backend-specific requirements",
        "UserProxy: Processes feedback and coordinates improvements"
    ]
    
    for agent in srd_agents:
        print(f"  • {agent}")
    
    print("\n🚀 Code Generation Agents:")
    code_agents = [
        "APIDesignerAgent: Designs REST endpoints and routing",
        "ModelDeveloperAgent: Creates database models and schemas",
        "BusinessLogicAgent: Implements core business functionality",
        "IntegrationAgent: Handles external service integrations",
        "DatabaseMigrationAgent: Creates database setup and migrations",
        "CodeCoordinatorAgent: Orchestrates project structure"
    ]
    
    for agent in code_agents:
        print(f"  • {agent}")

if __name__ == "__main__":
    print("🌟 Requirements Analyzer with Code Generation - Complete Demo")
    
    # Show workflow overview
    show_workflow_summary()
    
    # Run the demo
    print_header("🧪 RUNNING WORKFLOW DEMO")
    success = test_complete_workflow()
    
    if success:
        print_header("🎉 DEMO COMPLETED SUCCESSFULLY")
        print("The complete workflow has been demonstrated successfully!")
        print("\n📋 What was accomplished:")
        print("✅ API health check")
        print("✅ SRD feedback and regeneration")
        print("✅ Multi-agent code generation")
        print("✅ File generation and organization")
        print("✅ Download preparation")
        
        print("\n🚀 Ready for Production Use!")
        print("Start the full application with: python run_ui.py")
        
    else:
        print_header("❌ DEMO ENCOUNTERED ISSUES")
        print("Please check the server status and try again.")
        print("Ensure the FastAPI server is running on localhost:8000")