#!/usr/bin/env python3
"""
Test script for the Angular frontend code generation workflow
"""

import asyncio
import requests
import json

API_BASE_URL = "http://localhost:8000"

# Sample Frontend SRD for testing
SAMPLE_FRONTEND_SRD = """
# Frontend Software Requirements Document

## 1. System Overview
This frontend application provides a user interface for a task management system with user authentication, task management, and team collaboration features built with Angular.

## 2. User Interface Requirements

### 2.1 Authentication Module
- Login page with email/password form
- Registration page with form validation
- Password reset functionality
- JWT token handling and storage
- Protected route guards

### 2.2 Dashboard Module
- Main dashboard with task overview
- Navigation sidebar with menu items
- User profile dropdown
- Task statistics widgets
- Quick task creation modal

### 2.3 Task Management Module
- Task list view with filtering and sorting
- Task creation form with validation
- Task editing capabilities
- Task status updates (drag & drop)
- Task assignment to team members
- Due date picker and reminders

### 2.4 Team Collaboration Module
- Team list and member management
- Team creation and editing forms
- Member invitation system
- Role-based access controls
- Team task assignment interface

## 3. Technical Requirements

### 3.1 Framework and Libraries
- Angular 16+ with TypeScript
- Angular Material for UI components
- RxJS for reactive programming
- NgRx for state management
- Angular Reactive Forms
- Angular Router for navigation

### 3.2 Component Architecture
- Shared components (Header, Sidebar, Modal)
- Feature modules (Auth, Dashboard, Tasks, Teams)
- Smart/Container components for data management
- Presentational components for UI display
- Reusable form components

### 3.3 Services and Data Management
- Authentication service with JWT handling
- HTTP interceptors for token management
- Task service for CRUD operations
- Team service for collaboration features
- User service for profile management
- Error handling service

### 3.4 State Management
- NgRx store for application state
- Actions for user interactions
- Reducers for state updates
- Effects for side effects (API calls)
- Selectors for data access

### 3.5 Routing Structure
- Public routes: /login, /register, /forgot-password
- Protected routes: /dashboard, /tasks, /teams, /profile
- Route guards for authentication
- Lazy loading for feature modules

## 4. UI/UX Requirements

### 4.1 Design System
- Material Design principles
- Consistent color scheme and typography
- Responsive design for mobile and desktop
- Accessibility (WCAG 2.1 compliance)
- Loading states and skeleton screens

### 4.2 User Experience
- Intuitive navigation and workflow
- Real-time updates for collaborative features
- Smooth transitions and animations
- Form validation with clear error messages
- Confirmation dialogs for destructive actions

### 4.3 Responsive Behavior
- Mobile-first design approach
- Responsive grid layout
- Collapsible sidebar for mobile
- Touch-friendly controls
- Adaptive component sizing

## 5. Forms and Validation

### 5.1 Form Requirements
- Reactive forms with TypeScript typing
- Client-side validation with error messages
- Dynamic form controls based on user roles
- Auto-save functionality for long forms
- File upload capabilities

### 5.2 Validation Rules
- Email format validation
- Password strength requirements
- Required field validation
- Custom validators for business rules
- Async validation for unique constraints

## 6. Performance Requirements

### 6.1 Loading and Performance
- Initial page load under 3 seconds
- Lazy loading for feature modules
- OnPush change detection strategy
- Virtual scrolling for large lists
- Image optimization and lazy loading

### 6.2 User Experience Performance
- Smooth animations (60fps)
- Instant feedback for user actions
- Optimistic UI updates
- Efficient data fetching with caching
- Minimal bundle size optimization

## 7. Error Handling and Feedback

### 7.1 Error Management
- Global error handling service
- User-friendly error messages
- Retry mechanisms for failed requests
- Offline mode notifications
- Graceful degradation

### 7.2 User Feedback
- Success notifications for completed actions
- Progress indicators for long operations
- Confirmation dialogs for important actions
- Toast notifications for status updates
- Loading spinners and skeleton screens
"""

async def test_frontend_generation():
    """Test the Angular frontend code generation API"""
    print("🧪 Testing Angular Frontend Code Generation")
    print("=" * 50)
    
    try:
        # Test the frontend code generation endpoint
        payload = {
            "frontend_srd": SAMPLE_FRONTEND_SRD,
            "project_name": "task_management_frontend",
            "framework": "angular",
            "output_format": "files"
        }
        
        print("📤 Sending frontend SRD for Angular code generation...")
        print(f"📄 SRD Length: {len(SAMPLE_FRONTEND_SRD)} characters")
        print(f"🏗️ Framework: Angular")
        
        response = requests.post(f"{API_BASE_URL}/generate-frontend-code", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['message']}")
            print(f"📁 Project Path: {result.get('project_path', 'N/A')}")
            print(f"📊 Angular Files Generated: {result.get('file_count', 0)}")
            print(f"🏗️ Framework: {result.get('framework', 'Angular')}")
            
            # Show generated files summary
            if result.get('generated_files'):
                print("\n📝 Generated Angular Files:")
                
                # Categorize files
                ts_files = []
                html_files = []
                scss_files = []
                json_files = []
                other_files = []
                
                for file_path in result['generated_files'].keys():
                    content_length = len(result['generated_files'][file_path])
                    if file_path.endswith('.ts'):
                        ts_files.append(f"  📝 {file_path} ({content_length} chars)")
                    elif file_path.endswith('.html'):
                        html_files.append(f"  🎨 {file_path} ({content_length} chars)")
                    elif file_path.endswith('.scss'):
                        scss_files.append(f"  💄 {file_path} ({content_length} chars)")
                    elif file_path.endswith('.json'):
                        json_files.append(f"  ⚙️ {file_path} ({content_length} chars)")
                    else:
                        other_files.append(f"  📄 {file_path} ({content_length} chars)")
                
                # Print categorized files
                if ts_files:
                    print("\n  TypeScript Files:")
                    for file_info in ts_files[:3]:  # Show first 3
                        print(file_info)
                    if len(ts_files) > 3:
                        print(f"    ... and {len(ts_files) - 3} more TypeScript files")
                
                if html_files:
                    print("\n  HTML Templates:")
                    for file_info in html_files[:2]:  # Show first 2
                        print(file_info)
                    if len(html_files) > 2:
                        print(f"    ... and {len(html_files) - 2} more HTML files")
                
                if scss_files:
                    print("\n  SCSS Styles:")
                    for file_info in scss_files[:2]:  # Show first 2
                        print(file_info)
                    if len(scss_files) > 2:
                        print(f"    ... and {len(scss_files) - 2} more SCSS files")
                
                if json_files:
                    print("\n  Configuration Files:")
                    for file_info in json_files:
                        print(file_info)
                
                if other_files:
                    print("\n  Other Files:")
                    for file_info in other_files:
                        print(file_info)
                
                # Show a preview of a TypeScript file
                ts_file_keys = [k for k in result['generated_files'].keys() if k.endswith('.ts')]
                if ts_file_keys:
                    preview_file = ts_file_keys[0]
                    preview_content = result['generated_files'][preview_file][:400]
                    print(f"\n👀 Preview of {preview_file}:")
                    print("-" * 50)
                    print(preview_content + "..." if len(result['generated_files'][preview_file]) > 400 else preview_content)
                    print("-" * 50)
            
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

def test_angular_agent_descriptions():
    """Show what each Angular agent is responsible for"""
    print("\n🤖 Angular Multi-Agent Code Generation System")
    print("=" * 50)
    
    agents = {
        "ComponentDesignerAgent": "Designs Angular components, TypeScript classes, and component architecture",
        "ServiceDeveloperAgent": "Creates Angular services, HTTP clients, and data management logic", 
        "UIImplementationAgent": "Implements HTML templates, SCSS styles, and Angular Material UI",
        "StateManagementAgent": "Designs NgRx state management, actions, reducers, and effects",
        "FrontendCoordinatorAgent": "Orchestrates Angular project structure and module configuration"
    }
    
    for agent_name, description in agents.items():
        print(f"🎯 {agent_name}")
        print(f"   {description}")
        print()

def compare_with_backend():
    """Compare frontend and backend generation capabilities"""
    print("\n🏗️ Frontend vs Backend Code Generation")
    print("=" * 50)
    
    comparison = {
        "Backend (FastAPI)": [
            "🏗️ APIDesignerAgent → REST endpoints and routing",
            "📊 ModelDeveloperAgent → Database models and schemas",
            "🧠 BusinessLogicAgent → Core business functionality",
            "🔗 IntegrationAgent → External service connections",
            "🗃️ DatabaseMigrationAgent → Database setup and migrations",
            "🎯 CodeCoordinatorAgent → Project structure integration"
        ],
        "Frontend (Angular)": [
            "🏗️ ComponentDesignerAgent → Angular components and architecture",
            "🔧 ServiceDeveloperAgent → Angular services and HTTP clients",
            "🎨 UIImplementationAgent → Templates, styles, and Material UI",
            "🗄️ StateManagementAgent → NgRx state management patterns",
            "🎯 FrontendCoordinatorAgent → Angular project configuration"
        ]
    }
    
    for category, agents in comparison.items():
        print(f"\n{category}:")
        for agent in agents:
            print(f"  {agent}")

if __name__ == "__main__":
    print("🚀 Starting Angular Frontend Code Generation Tests")
    
    # Show Angular agent information
    test_angular_agent_descriptions()
    
    # Compare with backend
    compare_with_backend()
    
    # Test API health
    api_healthy = test_api_health()
    
    if api_healthy:
        print("\n" + "="*50)
        # Test the frontend generation workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            test_passed = loop.run_until_complete(test_frontend_generation())
        finally:
            loop.close()
        
        if test_passed:
            print("\n🎉 Angular frontend generation test completed successfully!")
            print("\n📋 Next Steps:")
            print("1. Start the application: python run_ui.py")
            print("2. Upload a document and generate SRDs")
            print("3. Use the 'Generate Angular Code' button")
            print("4. Review the generated Angular files")
            print("5. Download the complete Angular project")
            print("\n🏗️ Full Stack Development:")
            print("- Generate both Frontend (Angular) and Backend (FastAPI)")
            print("- Create a complete, deployable application")
            print("- Professional separation of concerns")
        else:
            print("\n❌ Angular frontend generation test failed.")
    else:
        print("\n❌ API health check failed. Please start the server first.")