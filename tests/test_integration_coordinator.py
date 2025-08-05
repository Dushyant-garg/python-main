"""
Tests for IntegrationCoordinator agent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.integration_coordinator import IntegrationCoordinator


class TestIntegrationCoordinator:
    """Test suite for IntegrationCoordinator"""
    
    @pytest.fixture
    def coordinator(self, environment_vars):
        """Create IntegrationCoordinator instance for testing"""
        with patch('app.agents.integration_coordinator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return IntegrationCoordinator()
    
    @pytest.mark.unit
    def test_init(self, coordinator):
        """Test IntegrationCoordinator initialization"""
        assert coordinator is not None
        assert hasattr(coordinator, 'api_integration_agent')
        assert hasattr(coordinator, 'auth_integration_agent')
        assert hasattr(coordinator, 'deployment_coordinator_agent')
        assert hasattr(coordinator, 'integration_coordinator_agent')
    
    @pytest.mark.unit
    def test_system_messages(self, coordinator):
        """Test that all integration agent system messages are properly defined"""
        messages = {
            'api_integration': coordinator._get_api_integration_system_message(),
            'auth_integration': coordinator._get_auth_integration_system_message(),
            'deployment_coordinator': coordinator._get_deployment_coordinator_system_message(),
            'integration_coordinator': coordinator._get_integration_coordinator_system_message()
        }
        
        for agent_name, message in messages.items():
            assert len(message) > 100, f"{agent_name} message too short"
            assert "RESPONSIBILITIES" in message, f"{agent_name} missing responsibilities"
            assert "CRITICAL GUIDELINES" in message, f"{agent_name} missing guidelines"
            assert "OUTPUT FORMAT" in message, f"{agent_name} missing output format"
    
    @pytest.mark.unit
    def test_api_integration_message_content(self, coordinator):
        """Test APIIntegration system message contains API integration elements"""
        message = coordinator._get_api_integration_system_message()
        
        required_terms = [
            "APIIntegrationAgent", "Angular", "FastAPI", "HTTP", "TypeScript", 
            "interfaces", "Pydantic", "environment", "HttpClient"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_auth_integration_message_content(self, coordinator):
        """Test AuthIntegration system message contains auth elements"""
        message = coordinator._get_auth_integration_system_message()
        
        required_terms = [
            "AuthIntegrationAgent", "JWT", "authentication", "token", 
            "Angular", "FastAPI", "interceptor", "guard"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_deployment_coordinator_message_content(self, coordinator):
        """Test DeploymentCoordinator system message contains deployment elements"""
        message = coordinator._get_deployment_coordinator_system_message()
        
        required_terms = [
            "DeploymentCoordinatorAgent", "Docker", "docker-compose", 
            "environment", "CORS", "networking", "Nginx"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_integration_package_success(self, coordinator, mock_generated_code, sample_frontend_srd, sample_backend_srd):
        """Test successful integration package generation"""
        # Create mock frontend and backend files
        frontend_files = {
            "src/app/app.component.ts": "Angular component content",
            "src/app/user.service.ts": "Angular service content"
        }
        
        backend_files = {
            "app/main.py": "FastAPI main content",
            "app/models.py": "SQLAlchemy models content"
        }
        
        with patch('app.agents.integration_coordinator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock integration conversation
            mock_messages = [
                Mock(content="""
# docker-compose.yml
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["4200:4200"]
    depends_on: [backend]
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - CORS_ORIGINS=http://localhost:4200
```
""", source="DeploymentCoordinatorAgent"),
                Mock(content="""
// src/app/services/api.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;
  
  constructor(private http: HttpClient) {}
  
  getUsers() {
    return this.http.get(`${this.apiUrl}/api/users`);
  }
}
```
""", source="APIIntegrationAgent"),
                Mock(content="""
// src/app/auth/auth.interceptor.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const token = localStorage.getItem('access_token');
    if (token) {
      const authReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`)
      });
      return next.handle(authReq);
    }
    return next.handle(req);
  }
}
```
""", source="AuthIntegrationAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            result = await coordinator.generate_integration_package(
                frontend_files, backend_files, "test_integration_project"
            )
            
            assert result is not None
            assert isinstance(result, dict)
            assert len(result) > 0
            
            # Should contain both original files and integration files
            frontend_paths = [path for path in result.keys() if "/frontend/" in path]
            backend_paths = [path for path in result.keys() if "/backend/" in path]
            integration_paths = [path for path in result.keys() if "/frontend/" not in path and "/backend/" not in path]
            
            assert len(frontend_paths) > 0, "Should include frontend files"
            assert len(backend_paths) > 0, "Should include backend files"
            assert len(integration_paths) > 0, "Should include integration files"
    
    @pytest.mark.unit
    def test_analyze_generated_files(self, coordinator):
        """Test analysis of generated files"""
        frontend_files = {
            "src/app/app.component.ts": "component content",
            "src/app/user.service.ts": "service content",
            "src/app/app.component.html": "template content",
            "src/app/app.component.scss": "styles content"
        }
        
        backend_files = {
            "app/main.py": "fastapi content",
            "app/models.py": "sqlalchemy content",
            "app/api.py": "api routes content"
        }
        
        frontend_analysis = coordinator._analyze_generated_files(frontend_files, "Angular Frontend")
        backend_analysis = coordinator._analyze_generated_files(backend_files, "FastAPI Backend")
        
        # Frontend analysis should identify Angular files
        assert "TypeScript Files: 2" in frontend_analysis
        assert "HTML Templates: 1" in frontend_analysis
        assert "SCSS Styles: 1" in frontend_analysis
        assert "Services: 1" in frontend_analysis
        
        # Backend analysis should identify Python files
        assert "Python Files: 3" in backend_analysis
        assert "API Files: 1" in backend_analysis
    
    @pytest.mark.unit
    def test_extract_integration_files(self, coordinator):
        """Test extraction of integration files from conversation"""
        messages = [
            Mock(content="""
# docker-compose.yml
```yaml
version: '3.8'
services:
  app: {}
```

# README.md
```markdown
# Integration Project
Setup instructions
```
""", source="TestAgent")
        ]
        
        result = coordinator._extract_integration_files(messages, "test_project")
        
        assert isinstance(result, dict)
        assert len(result) > 0
        
        # Should extract both YAML and Markdown
        yaml_files = [f for f in result.keys() if f.endswith('.yml')]
        md_files = [f for f in result.keys() if f.endswith('.md')]
        
        assert len(yaml_files) > 0
        assert len(md_files) > 0
    
    @pytest.mark.unit
    def test_create_integrated_package(self, coordinator):
        """Test creation of integrated package structure"""
        frontend_files = {"app.component.ts": "component"}
        backend_files = {"main.py": "fastapi"}
        integration_files = {"docker-compose.yml": "version: '3.8'"}
        
        result = coordinator._create_integrated_package(
            frontend_files, backend_files, integration_files, "test_project"
        )
        
        assert isinstance(result, dict)
        
        # Check structure
        frontend_paths = [path for path in result.keys() if "/frontend/" in path]
        backend_paths = [path for path in result.keys() if "/backend/" in path]
        
        assert len(frontend_paths) > 0
        assert len(backend_paths) > 0
        assert any("docker-compose" in path for path in result.keys())
        assert any("README" in path for path in result.keys())
    
    @pytest.mark.unit
    def test_default_integration_files(self, coordinator):
        """Test default integration file generation"""
        docker_compose = coordinator._get_default_docker_compose()
        readme = coordinator._get_default_integration_readme("test_project")
        env_file = coordinator._get_default_env_file()
        
        # Docker compose should contain services
        assert "version:" in docker_compose
        assert "services:" in docker_compose
        assert "frontend:" in docker_compose
        assert "backend:" in docker_compose
        assert "db:" in docker_compose
        
        # README should contain project info
        assert "test_project" in readme
        assert "Angular" in readme
        assert "FastAPI" in readme
        assert "Docker" in readme
        
        # Env file should contain configuration
        assert "DATABASE_URL" in env_file
        assert "SECRET_KEY" in env_file
        assert "CORS_ORIGINS" in env_file
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_integrated_package(self, coordinator, temp_output_dir):
        """Test saving integrated package to disk"""
        integrated_files = {
            "test_project/frontend/app.component.ts": "component content",
            "test_project/backend/main.py": "fastapi content",
            "test_project/docker-compose.yml": "version: '3.8'",
            "test_project/README.md": "# Test Project"
        }
        
        project_path = await coordinator.save_integrated_package(integrated_files, temp_output_dir)
        
        assert project_path is not None
        assert temp_output_dir in project_path
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_integration_error_handling(self, coordinator):
        """Test error handling in integration generation"""
        frontend_files = {"app.ts": "content"}
        backend_files = {"main.py": "content"}
        
        with patch('app.agents.integration_coordinator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            mock_instance.run.side_effect = Exception("Test error")
            
            result = await coordinator.generate_integration_package(
                frontend_files, backend_files, "test_project"
            )
            
            assert result is not None
            assert "error" in result
    
    @pytest.mark.unit
    def test_integration_file_patterns(self, coordinator):
        """Test recognition of various integration file patterns"""
        test_patterns = [
            # Docker files
            """# Dockerfile
```dockerfile
FROM node:18
WORKDIR /app
```""",
            # YAML files
            """# docker-compose.yml
```yaml
version: '3.8'
```""",
            # Environment files
            """# .env.example
```bash
DATABASE_URL=postgres://
```""",
            # TypeScript integration
            """# api.service.ts
```typescript
export class ApiService {}
```"""
        ]
        
        for pattern in test_patterns:
            messages = [Mock(content=pattern, source="TestAgent")]
            result = coordinator._extract_integration_files(messages, "test")
            assert len(result) > 0, f"Failed to extract from pattern: {pattern[:50]}..."


class TestIntegrationCoordinatorSpecialization:
    """Test integration agent specialization"""
    
    @pytest.fixture
    def coordinator(self, environment_vars):
        """Create coordinator for specialization testing"""
        with patch('app.agents.integration_coordinator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return IntegrationCoordinator()
    
    @pytest.mark.unit
    def test_api_integration_specialization(self, coordinator):
        """Test APIIntegration focuses on API communication"""
        message = coordinator._get_api_integration_system_message()
        
        assert "API" in message
        assert "Angular" in message
        assert "FastAPI" in message
        assert "Focus EXCLUSIVELY on API integration" in message
    
    @pytest.mark.unit
    def test_auth_integration_specialization(self, coordinator):
        """Test AuthIntegration focuses on authentication"""
        message = coordinator._get_auth_integration_system_message()
        
        assert "authentication" in message.lower()
        assert "JWT" in message
        assert "token" in message.lower()
        assert "Focus EXCLUSIVELY on authentication" in message
    
    @pytest.mark.unit
    def test_deployment_coordinator_specialization(self, coordinator):
        """Test DeploymentCoordinator focuses on deployment"""
        message = coordinator._get_deployment_coordinator_system_message()
        
        assert "deployment" in message.lower()
        assert "Docker" in message
        assert "docker-compose" in message.lower()
        assert "Focus EXCLUSIVELY on deployment" in message
    
    @pytest.mark.unit
    def test_integration_coordinator_orchestration(self, coordinator):
        """Test IntegrationCoordinator focuses on overall coordination"""
        message = coordinator._get_integration_coordinator_system_message()
        
        assert "coordinator" in message.lower() or "orchestrat" in message.lower()
        assert "integration" in message.lower()
        assert "TEAM WORKFLOW" in message


class TestIntegrationCoordinatorIntegration:
    """Integration tests for IntegrationCoordinator"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_complete_integration_workflow(self, environment_vars, temp_output_dir):
        """Test complete integration coordination workflow"""
        with patch('app.agents.integration_coordinator.OpenAIChatCompletionClient') as mock_client, \
             patch('app.agents.integration_coordinator.RoundRobinGroupChat') as mock_chat:
            
            # Setup mocks
            mock_client.return_value = Mock()
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Create comprehensive integration conversation
            mock_messages = [
                # API Integration
                Mock(content="""
// src/app/services/api.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;
  
  constructor(private http: HttpClient) {}
  
  getUsers() {
    return this.http.get(`${this.apiUrl}/api/users`);
  }
  
  createUser(user: any) {
    return this.http.post(`${this.apiUrl}/api/users`, user);
  }
}
```

// src/app/interfaces/user.interface.ts
```typescript
export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export interface UserCreate {
  email: string;
  name: string;
  password: string;
}
```
""", source="APIIntegrationAgent"),
                
                # Auth Integration
                Mock(content="""
// src/app/auth/auth.service.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<any>(null);
  
  constructor(private http: HttpClient) {}
  
  login(credentials: any): Observable<any> {
    return this.http.post('/api/auth/login', credentials)
      .pipe(tap(response => {
        localStorage.setItem('access_token', response.access_token);
        this.currentUserSubject.next(response.user);
      }));
  }
  
  logout(): void {
    localStorage.removeItem('access_token');
    this.currentUserSubject.next(null);
  }
}
```

// src/app/auth/auth.interceptor.ts
```typescript
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const token = localStorage.getItem('access_token');
    if (token) {
      const authReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`)
      });
      return next.handle(authReq);
    }
    return next.handle(req);
  }
}
```
""", source="AuthIntegrationAgent"),
                
                # Deployment Coordination
                Mock(content="""
# docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "4200:4200"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: ng serve --host 0.0.0.0 --port 4200

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - CORS_ORIGINS=http://localhost:4200,http://localhost
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

# frontend/Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4200"]
```

# backend/Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
""", source="DeploymentCoordinatorAgent"),
                
                # Integration Coordination
                Mock(content="""
# README.md
```markdown
# Integrated Full-Stack Application

This project contains a complete Angular + FastAPI application with Docker integration.

## Quick Start

```bash
# Start the complete application
docker-compose up --build

# Access the application
# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Development Setup

### Frontend (Angular)
```bash
cd frontend
npm install
ng serve
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Integration Features

- ✅ API Integration: Angular services consume FastAPI endpoints
- ✅ Authentication: JWT-based auth flow
- ✅ CORS Configuration: Proper cross-origin handling
- ✅ Docker Setup: Complete containerization
- ✅ Type Safety: TypeScript interfaces match Pydantic models
```

# .env.example
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/myapp

# JWT Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# Frontend Configuration
ANGULAR_API_URL=http://localhost:8000
```
""", source="IntegrationCoordinatorAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            # Create sample frontend and backend files
            frontend_files = {
                "src/app/app.component.ts": "Angular component",
                "src/app/app.module.ts": "Angular module"
            }
            
            backend_files = {
                "app/main.py": "FastAPI main",
                "app/models.py": "SQLAlchemy models"
            }
            
            # Create coordinator and run complete workflow
            coordinator = IntegrationCoordinator()
            
            # Step 1: Generate integration package
            integrated_package = await coordinator.generate_integration_package(
                frontend_files, backend_files, "full_stack_integration"
            )
            
            assert integrated_package is not None
            assert isinstance(integrated_package, dict)
            assert len(integrated_package) > 0
            
            # Verify integration components
            docker_files = [f for f in integrated_package.keys() if 'docker' in f.lower()]
            readme_files = [f for f in integrated_package.keys() if 'readme' in f.lower()]
            env_files = [f for f in integrated_package.keys() if '.env' in f]
            
            assert len(docker_files) > 0, "Should generate Docker configurations"
            assert len(readme_files) > 0, "Should generate documentation"
            assert len(env_files) > 0, "Should generate environment configuration"
            
            # Step 2: Save integrated package
            project_path = await coordinator.save_integrated_package(integrated_package, temp_output_dir)
            
            assert project_path is not None
            assert temp_output_dir in project_path
            
            # Verify content quality
            if docker_files:
                docker_content = integrated_package[docker_files[0]]
                assert "version:" in docker_content
                assert "frontend:" in docker_content
                assert "backend:" in docker_content