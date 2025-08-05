"""
Integration Coordinator Agent

This module manages the integration between generated frontend and backend code,
ensuring proper API communication, authentication flow, and deployment coordination.
"""

import os
import asyncio
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.termination import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

from app.config import settings


class IntegrationCoordinator:
    """
    Coordinates integration between Angular frontend and FastAPI backend
    """
    
    def __init__(self):
        """Initialize the IntegrationCoordinator with specialized agents"""
        
        # Initialize the OpenAI client
        self.model_client = OpenAIChatCompletionClient(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.1,  # Low temperature for precise integration code
        )
        
        # Integration specialist agents
        self.api_integration_agent = AssistantAgent(
            name="APIIntegrationAgent",
            model_client=self.model_client,
            system_message=self._get_api_integration_system_message(),
        )
        
        self.auth_integration_agent = AssistantAgent(
            name="AuthIntegrationAgent",
            model_client=self.model_client,
            system_message=self._get_auth_integration_system_message(),
        )
        
        self.deployment_coordinator_agent = AssistantAgent(
            name="DeploymentCoordinatorAgent",
            model_client=self.model_client,
            system_message=self._get_deployment_coordinator_system_message(),
        )
        
        self.integration_coordinator_agent = AssistantAgent(
            name="IntegrationCoordinatorAgent",
            model_client=self.model_client,
            system_message=self._get_integration_coordinator_system_message(),
        )
    
    def _get_api_integration_system_message(self) -> str:
        """Get system message for the API Integration agent"""
        return """You are the APIIntegrationAgent, responsible for creating seamless API communication between Angular frontend and FastAPI backend.

RESPONSIBILITIES:
1. Generate Angular HTTP services that match FastAPI endpoints
2. Create TypeScript interfaces that match Pydantic models
3. Implement error handling and retry logic
4. Set up HTTP interceptors for authentication and error handling
5. Configure environment-based API URLs

CRITICAL GUIDELINES:
- Ensure Angular services match FastAPI endpoint signatures exactly
- Use consistent data models between frontend and backend
- Implement proper error handling and user feedback
- Use Angular HttpClient with proper typing
- Configure base URLs through environment files

OUTPUT FORMAT:
Generate Angular integration files:
- API service classes (.service.ts)
- TypeScript interfaces matching backend models (.interface.ts)
- HTTP interceptors (.interceptor.ts)
- Environment configuration files
- Error handling utilities

EXAMPLE OUTPUT STRUCTURE:
```typescript
// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Match FastAPI endpoints exactly
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/api/users`);
  }

  createUser(userData: UserCreate): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/api/users`, userData);
  }
}

// user.interface.ts
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

Focus EXCLUSIVELY on API integration and data flow between frontend and backend.
"""

    def _get_auth_integration_system_message(self) -> str:
        """Get system message for the Auth Integration agent"""
        return """You are the AuthIntegrationAgent, responsible for coordinating authentication and authorization between Angular frontend and FastAPI backend.

RESPONSIBILITIES:
1. Create Angular authentication service that works with FastAPI JWT
2. Implement token storage and refresh mechanisms
3. Set up HTTP interceptors for automatic token inclusion
4. Create route guards for protected areas
5. Handle authentication state management

CRITICAL GUIDELINES:
- Use secure token storage (HttpOnly cookies or secure localStorage)
- Implement automatic token refresh before expiration
- Handle authentication errors gracefully
- Provide clear user feedback for auth states
- Secure route protection with guards

OUTPUT FORMAT:
Generate authentication integration files:
- Authentication service (.service.ts)
- JWT interceptor (.interceptor.ts)
- Route guards (.guard.ts)
- Authentication state management
- Login/logout components

EXAMPLE OUTPUT STRUCTURE:
```typescript
// auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {}

  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>('/api/auth/login', credentials)
      .pipe(
        tap(response => {
          localStorage.setItem('access_token', response.access_token);
          this.currentUserSubject.next(response.user);
        })
      );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    this.currentUserSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }
}

// auth.interceptor.ts
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

Focus EXCLUSIVELY on authentication and authorization integration.
"""

    def _get_deployment_coordinator_system_message(self) -> str:
        """Get system message for the Deployment Coordinator agent"""
        return """You are the DeploymentCoordinatorAgent, responsible for creating deployment configurations and orchestration for the full-stack application.

RESPONSIBILITIES:
1. Create Docker configurations for both frontend and backend
2. Set up docker-compose for full-stack deployment
3. Generate environment configurations for different stages
4. Create deployment scripts and CI/CD configurations
5. Configure CORS and networking between services

CRITICAL GUIDELINES:
- Use multi-stage Docker builds for optimization
- Configure proper networking between frontend and backend containers
- Set up environment-specific configurations
- Implement health checks and monitoring
- Secure communication between services

OUTPUT FORMAT:
Generate deployment configuration files:
- Dockerfile for Angular frontend
- Dockerfile for FastAPI backend
- docker-compose.yml for full-stack orchestration
- Environment files (.env)
- Deployment scripts
- Nginx configuration for production

EXAMPLE OUTPUT STRUCTURE:
```dockerfile
# Frontend Dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      - db
      
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
      
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

Focus EXCLUSIVELY on deployment and infrastructure coordination.
"""

    def _get_integration_coordinator_system_message(self) -> str:
        """Get system message for the Integration Coordinator agent"""
        return """You are the IntegrationCoordinatorAgent, responsible for orchestrating the overall integration between Angular frontend and FastAPI backend.

RESPONSIBILITIES:
1. Coordinate all integration aspects (API, Auth, Deployment)
2. Generate integration documentation and setup guides
3. Create development environment setup scripts
4. Ensure consistent configuration across frontend and backend
5. Generate testing scripts for full-stack integration

CRITICAL GUIDELINES:
- Ensure seamless communication between all components
- Provide clear documentation for developers
- Create automated setup and testing scripts
- Handle environment-specific configurations
- Coordinate version compatibility between frontend and backend

OUTPUT FORMAT:
Generate coordination files:
- Integration documentation (README.md)
- Setup scripts (setup.sh, setup.ps1)
- Environment configuration templates
- Integration testing scripts
- Development workflow guides

TEAM WORKFLOW:
1. Analyze frontend and backend code structures
2. Coordinate API integration requirements
3. Set up authentication flow
4. Configure deployment orchestration
5. Generate comprehensive integration package

Focus on overall coordination and ensuring all components work together seamlessly.
"""

    async def generate_integration_package(
        self, 
        frontend_files: Dict[str, str], 
        backend_files: Dict[str, str],
        project_name: str = "integrated_fullstack_app"
    ) -> Dict[str, str]:
        """
        Generate complete integration package for frontend and backend
        
        Args:
            frontend_files: Generated Angular frontend files
            backend_files: Generated FastAPI backend files
            project_name: Name for the integrated project
            
        Returns:
            Dictionary containing integration files and configurations
        """
        
        # Create integration task
        integration_task = f"""
FULL-STACK INTEGRATION PROJECT

PROJECT NAME: {project_name}

FRONTEND FILES ANALYSIS:
{self._analyze_generated_files(frontend_files, "Angular Frontend")}

BACKEND FILES ANALYSIS:
{self._analyze_generated_files(backend_files, "FastAPI Backend")}

INTEGRATION REQUIREMENTS:
1. API Communication: Angular services must match FastAPI endpoints
2. Authentication Flow: JWT authentication between frontend and backend
3. CORS Configuration: Proper cross-origin request handling
4. Environment Setup: Development and production configurations
5. Deployment Coordination: Docker containers and orchestration
6. Error Handling: Consistent error responses and frontend handling
7. Data Models: TypeScript interfaces matching Pydantic models

TEAM WORKFLOW:
1. IntegrationCoordinatorAgent: Analyze requirements and plan integration
2. APIIntegrationAgent: Create Angular services matching FastAPI endpoints
3. AuthIntegrationAgent: Set up authentication flow and security
4. DeploymentCoordinatorAgent: Create deployment configurations
5. IntegrationCoordinatorAgent: Finalize integration package and documentation

Generate a complete integration package that allows the frontend and backend to work together seamlessly.

BEGIN INTEGRATION GENERATION:
"""

        try:
            # Create the integration team
            integration_team = RoundRobinGroupChat(
                participants=[
                    self.integration_coordinator_agent,
                    self.api_integration_agent,
                    self.auth_integration_agent,
                    self.deployment_coordinator_agent,
                    self.integration_coordinator_agent  # Final coordination
                ],
                termination_condition=MaxMessageTermination(12)
            )
            
            # Start the integration process
            task_message = TextMessage(content=integration_task, source="user")
            result = await integration_team.run(task=task_message)
            
            # Extract integration files from the conversation
            integration_files = self._extract_integration_files(result.messages, project_name)
            
            # Add the original frontend and backend files to the integration package
            integrated_package = self._create_integrated_package(
                frontend_files, backend_files, integration_files, project_name
            )
            
            return integrated_package
            
        except Exception as e:
            print(f"Error generating integration package: {str(e)}")
            return {"error": f"Integration generation failed: {str(e)}"}
    
    def _analyze_generated_files(self, files: Dict[str, str], project_type: str) -> str:
        """Analyze generated files to understand structure for integration"""
        
        analysis = f"\n{project_type} Structure Analysis:\n"
        
        if project_type == "Angular Frontend":
            ts_files = [f for f in files.keys() if f.endswith('.ts')]
            html_files = [f for f in files.keys() if f.endswith('.html')]
            scss_files = [f for f in files.keys() if f.endswith('.scss')]
            
            analysis += f"- TypeScript Files: {len(ts_files)}\n"
            analysis += f"- HTML Templates: {len(html_files)}\n"
            analysis += f"- SCSS Styles: {len(scss_files)}\n"
            
            # Look for key files
            services = [f for f in ts_files if 'service' in f.lower()]
            components = [f for f in ts_files if 'component' in f.lower()]
            
            analysis += f"- Services: {len(services)}\n"
            analysis += f"- Components: {len(components)}\n"
            
        elif project_type == "FastAPI Backend":
            py_files = [f for f in files.keys() if f.endswith('.py')]
            
            analysis += f"- Python Files: {len(py_files)}\n"
            
            # Look for key patterns
            models = [f for f in py_files if 'model' in f.lower()]
            apis = [f for f in py_files if any(term in f.lower() for term in ['api', 'router', 'endpoint'])]
            
            analysis += f"- Models: {len(models)}\n"
            analysis += f"- API Files: {len(apis)}\n"
        
        return analysis
    
    def _extract_integration_files(self, messages: List, project_name: str) -> Dict[str, str]:
        """Extract integration files from agent conversation"""
        
        integration_files = {}
        current_file = None
        current_content = []
        
        for message in messages:
            if not hasattr(message, 'content'):
                continue
                
            content = message.content
            lines = content.split('\n')
            
            for line in lines:
                # Look for file indicators
                if line.strip().startswith('```') and any(lang in line for lang in ['typescript', 'dockerfile', 'yaml', 'bash', 'json']):
                    if current_file and current_content:
                        integration_files[current_file] = '\n'.join(current_content)
                        current_content = []
                    
                elif line.strip() == '```':
                    if current_file and current_content:
                        integration_files[current_file] = '\n'.join(current_content)
                        current_file = None
                        current_content = []
                        
                elif line.strip().startswith('#') and any(ext in line for ext in ['.ts', '.yml', '.yaml', '.dockerfile', '.sh', '.ps1', '.md', '.json', '.conf']):
                    potential_file = line.strip('#').strip()
                    current_file = potential_file
                        
                elif current_file and line.strip():
                    current_content.append(line)
        
        # Handle any remaining content
        if current_file and current_content:
            integration_files[current_file] = '\n'.join(current_content)
        
        return integration_files
    
    def _create_integrated_package(
        self, 
        frontend_files: Dict[str, str], 
        backend_files: Dict[str, str], 
        integration_files: Dict[str, str],
        project_name: str
    ) -> Dict[str, str]:
        """Create complete integrated package with all files"""
        
        integrated_package = {}
        
        # Add frontend files with proper path structure
        for file_path, content in frontend_files.items():
            integrated_path = f"{project_name}/frontend/{file_path}"
            integrated_package[integrated_path] = content
        
        # Add backend files with proper path structure
        for file_path, content in backend_files.items():
            integrated_path = f"{project_name}/backend/{file_path}"
            integrated_package[integrated_path] = content
        
        # Add integration files
        for file_path, content in integration_files.items():
            if not file_path.startswith(project_name):
                integrated_path = f"{project_name}/{file_path}"
            else:
                integrated_path = file_path
            integrated_package[integrated_path] = content
        
        # Add default integration files if not generated
        if not any('docker-compose' in path for path in integrated_package.keys()):
            integrated_package[f"{project_name}/docker-compose.yml"] = self._get_default_docker_compose()
        
        if not any('README' in path for path in integrated_package.keys()):
            integrated_package[f"{project_name}/README.md"] = self._get_default_integration_readme(project_name)
        
        if not any('.env' in path for path in integrated_package.keys()):
            integrated_package[f"{project_name}/.env.example"] = self._get_default_env_file()
        
        return integrated_package
    
    def _get_default_docker_compose(self) -> str:
        """Generate default docker-compose configuration"""
        return """version: '3.8'

services:
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
"""

    def _get_default_integration_readme(self, project_name: str) -> str:
        """Generate default integration README"""
        return f"""# {project_name}

Full-stack application with Angular frontend and FastAPI backend.

## Architecture

```
{project_name}/
├── frontend/          # Angular application
├── backend/           # FastAPI application
├── docker-compose.yml # Development orchestration
└── README.md         # This file
```

## Quick Start

### Development with Docker

1. **Start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Development

#### Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   ng serve
   ```

## Integration Features

- ✅ **API Integration**: Angular services consume FastAPI endpoints
- ✅ **Authentication**: JWT-based auth flow between frontend and backend
- ✅ **CORS Configuration**: Proper cross-origin request handling
- ✅ **Error Handling**: Consistent error responses and frontend handling
- ✅ **Type Safety**: TypeScript interfaces matching Pydantic models
- ✅ **Environment Config**: Development and production configurations

## API Endpoints

The backend provides the following main endpoints:

- `POST /api/auth/login` - User authentication
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/docs` - API documentation

## Deployment

### Production Deployment

1. **Build for production:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

2. **Environment variables:**
   Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

## Development Workflow

1. **Make changes** to frontend or backend code
2. **Services auto-reload** with Docker volumes
3. **Test integration** through the frontend UI
4. **Check API docs** at http://localhost:8000/docs

## Troubleshooting

### CORS Issues
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check browser console for CORS errors

### Database Connection
- Verify PostgreSQL is running
- Check `DATABASE_URL` in environment variables

### Port Conflicts
- Change ports in `docker-compose.yml` if needed
- Default ports: Frontend (4200), Backend (8000), DB (5432)
"""

    def _get_default_env_file(self) -> str:
        """Generate default environment file template"""
        return """# Environment Configuration Template
# Copy this file to .env and update values for your environment

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/myapp

# JWT Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# API Configuration
API_V1_STR=/api/v1

# Frontend Configuration
ANGULAR_API_URL=http://localhost:8000

# Development/Production
DEBUG=true
ENVIRONMENT=development
"""

    async def save_integrated_package(self, integrated_files: Dict[str, str], output_dir: str = "integrated_projects") -> str:
        """
        Save integrated full-stack package to disk
        
        Args:
            integrated_files: Dictionary of file paths to content
            output_dir: Base directory for saving files
            
        Returns:
            Path to the saved integrated project directory
        """
        
        base_path = Path(output_dir)
        base_path.mkdir(exist_ok=True)
        
        for file_path, content in integrated_files.items():
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return str(base_path)