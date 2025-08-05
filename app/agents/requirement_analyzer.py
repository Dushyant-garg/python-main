from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from typing import Dict, Tuple
import os
from pathlib import Path
from app.config import settings

class RequirementAnalyzer:
    """
    AutoGen-based agent for analyzing project requirements and generating SRDs
    """
    
    def __init__(self):
        """Initialize the RequirementAnalyzer with AutoGen agents"""
        
        # Initialize the OpenAI client
        self.model_client = OpenAIChatCompletionClient(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.1,
        )
        
        # Create the requirement analyst agent
        self.analyst_agent = AssistantAgent(
            name="RequirementAnalyst",
            model_client=self.model_client,
            system_message=self._get_analyst_system_message(),
        )
        
        # Create the frontend specialist agent
        self.frontend_agent = AssistantAgent(
            name="FrontendSpecialist",
            model_client=self.model_client,
            system_message=self._get_frontend_system_message(),
        )
        
        # Create the backend specialist agent
        self.backend_agent = AssistantAgent(
            name="BackendSpecialist",
            model_client=self.model_client,
            system_message=self._get_backend_system_message(),
        )
    
    def _get_analyst_system_message(self) -> str:
        """Get system message for the requirement analyst"""
        return """You are a Senior Requirements Analyst specializing in analyzing project documents and extracting clear, actionable requirements.

CRITICAL: You must analyze and CATEGORIZE requirements clearly into FRONTEND and BACKEND sections.

Your analysis must include:

## FRONTEND REQUIREMENTS:
- User Interface (UI) components and layouts
- User Experience (UX) workflows and interactions
- Client-side functionality and features
- Responsive design and mobile considerations
- User authentication flows (login/signup interfaces)
- Form inputs, validations, and user feedback
- Navigation menus, routing, and page structures
- Data display and visualization requirements
- Real-time updates and notifications (client-side)
- Browser compatibility and accessibility

## BACKEND REQUIREMENTS:
- Server-side business logic and algorithms
- Database design and data models
- API endpoints and data processing
- Authentication and authorization mechanisms
- Server architecture and scalability
- Data validation and security measures
- Integration with external services
- File handling and storage systems
- Background jobs and scheduled tasks
- Performance optimization and caching

## INTEGRATION REQUIREMENTS:
- API contracts between frontend and backend
- Data exchange formats and protocols
- Third-party service integrations
- Security protocols and encryption

Provide a STRUCTURED analysis with clear separation between frontend and backend concerns. Be specific about what belongs to each domain."""
    
    def _get_frontend_system_message(self) -> str:
        """Get system message for the frontend specialist"""
        return """You are a Frontend Architecture Specialist. FOCUS EXCLUSIVELY on CLIENT-SIDE requirements.

IGNORE backend/server concerns. You ONLY handle:
- User Interface (UI) design and components
- User Experience (UX) flows and interactions
- Client-side functionality and JavaScript behavior
- Frontend frameworks and libraries
- Browser rendering and compatibility
- Responsive design and mobile interfaces

Create a FRONTEND-ONLY SRD with this structure:

# Frontend Software Requirements Document

## 1. User Interface Requirements
- Layout and visual design specifications
- Component library and design system
- Navigation and menu structures
- Forms, inputs, and user controls
- Modal dialogs and overlays
- Loading states and feedback

## 2. User Experience Requirements
- User workflows and interaction patterns
- Page transitions and routing
- Form validation and error handling
- Accessibility features (ARIA, keyboard navigation)
- Responsive breakpoints and mobile experience
- Offline functionality and PWA features

## 3. Client-Side Functionality
- Frontend state management
- Data fetching and caching strategies
- Real-time updates (WebSocket handling)
- File upload interfaces
- Search and filtering capabilities
- Client-side validation logic

## 4. Technology Stack
- Frontend framework (React, Vue, Angular, etc.)
- State management libraries
- CSS frameworks and styling approach
- Build tools and bundlers
- Testing frameworks for frontend
- Browser compatibility requirements

## 5. Performance Requirements
- Page load time targets
- Bundle size optimization
- Code splitting strategies
- Image optimization and lazy loading
- Caching strategies (browser cache)
- Core Web Vitals targets

## 6. API Integration
- REST API consumption patterns
- Error handling for API calls
- Authentication token management
- Data transformation and formatting
- API response caching

Generate ONLY frontend-specific requirements. Do NOT include server, database, or backend logic."""
    
    def _get_backend_system_message(self) -> str:
        """Get system message for the backend specialist"""
        return """You are a Backend Architecture Specialist. FOCUS EXCLUSIVELY on SERVER-SIDE requirements.

IGNORE frontend/UI concerns. You ONLY handle:
- Server-side business logic and algorithms
- Database design and data persistence
- API development and web services
- Authentication and authorization systems
- Server infrastructure and deployment
- Data processing and background jobs

Create a BACKEND-ONLY SRD with this structure:

# Backend Software Requirements Document

## 1. System Architecture
- Server architecture and design patterns
- Microservices vs monolithic approach
- Load balancing and scaling strategies
- Service mesh and communication patterns
- Deployment architecture (containers, cloud)

## 2. Database Requirements
- Database design and schema specifications
- Data models and entity relationships
- Database choice (SQL/NoSQL) with justification
- Data migration and versioning strategies
- Backup and disaster recovery procedures
- Data retention and archival policies

## 3. API Specifications
- REST API endpoint definitions
- Request/response schemas and data formats
- API versioning and backward compatibility
- Rate limiting and throttling mechanisms
- API documentation and OpenAPI specs
- GraphQL schema (if applicable)

## 4. Business Logic Requirements
- Core business rules and algorithms
- Data processing workflows
- Validation and business rule enforcement
- Calculation engines and complex operations
- Integration with external services
- Event processing and message handling

## 5. Authentication & Authorization
- User authentication mechanisms (JWT, OAuth, etc.)
- Role-based access control (RBAC)
- Permission systems and policy enforcement
- Session management and token handling
- Multi-factor authentication requirements
- Security audit trails

## 6. Performance & Scalability
- Response time and throughput requirements
- Horizontal and vertical scaling strategies
- Caching mechanisms (Redis, Memcached)
- Database query optimization
- Background job processing
- Load testing and performance monitoring

## 7. Infrastructure & DevOps
- Server provisioning and configuration
- CI/CD pipeline requirements
- Monitoring and alerting systems
- Logging and error tracking
- Backup and disaster recovery
- Security scanning and compliance

## 8. Integration Requirements
- Third-party API integrations
- Message queues and event systems
- File storage and content delivery
- Email and notification services
- Payment processing systems
- Analytics and reporting services

Generate ONLY backend/server-side requirements. Do NOT include UI, frontend frameworks, or client-side logic."""
    
    async def analyze_requirements(self, document_text: str) -> Dict[str, str]:
        """
        Analyze document text and generate frontend and backend SRDs
        
        Args:
            document_text: The parsed text from the uploaded document
            
        Returns:
            Dictionary containing 'frontend_srd' and 'backend_srd' content
        """
        
        # Step 1: Analyze requirements with the analyst agent
        analysis_prompt = f"""
        REQUIREMENTS ANALYST TASK: Analyze the following project document and categorize ALL requirements clearly.

        PROJECT DOCUMENT:
        {document_text}

        CRITICAL: You must provide a STRUCTURED analysis that clearly separates frontend and backend concerns. Use the following format:

        # REQUIREMENTS ANALYSIS

        ## FRONTEND REQUIREMENTS
        List ALL client-side, UI, and user experience requirements including:
        - User interface components and layouts
        - User interaction workflows and experiences  
        - Client-side functionality and features
        - Form designs and user input handling
        - Navigation and routing requirements
        - Responsive design and mobile considerations
        - Frontend performance and optimization needs

        ## BACKEND REQUIREMENTS  
        List ALL server-side, database, and system architecture requirements including:
        - Server-side business logic and algorithms
        - Database design and data storage needs
        - API endpoints and web service specifications
        - Authentication and authorization systems
        - Server architecture and scalability requirements
        - Data processing and background job requirements
        - Integration with external services and APIs

        ## SHARED/INTEGRATION REQUIREMENTS
        List requirements that involve both frontend and backend:
        - API contracts and data exchange formats
        - Authentication flows and security protocols
        - Real-time communication requirements
        - File upload/download workflows

        Ensure each requirement is placed in the correct category and be specific about implementation domains.
        """
        
        # Create task message for analysis
        analysis_task = TextMessage(content=analysis_prompt, source="user")
        
        # Create a team with the analyst agent for analysis
        analysis_team = RoundRobinGroupChat(
            participants=[self.analyst_agent],
            termination_condition=MaxMessageTermination(1)
        )
        
        # Run analysis
        analysis_result = await analysis_team.run(task=analysis_task)
        analysis_content = analysis_result.messages[-1].content
        
        # Step 2: Generate frontend SRD
        frontend_prompt = f"""
        FRONTEND SPECIALIST TASK: Create a detailed Frontend SRD document.

        CRITICAL INSTRUCTIONS:
        - Focus ONLY on client-side, user interface, and user experience requirements
        - DO NOT include backend, server, database, or API implementation details
        - Extract ONLY frontend-related requirements from the analysis below

        REQUIREMENTS ANALYSIS:
        {analysis_content}

        DELIVERABLE: Create a comprehensive Frontend Software Requirements Document that focuses exclusively on:
        1. User Interface components and layouts
        2. User Experience workflows and interactions
        3. Client-side functionality and JavaScript behavior
        4. Frontend technology stack and frameworks
        5. Browser compatibility and responsive design
        6. Frontend performance and optimization
        7. API consumption patterns (client-side perspective only)

        Generate a professional SRD document in markdown format with detailed frontend specifications.
        """
        
        frontend_task = TextMessage(content=frontend_prompt, source="user")
        frontend_team = RoundRobinGroupChat(
            participants=[self.frontend_agent],
            termination_condition=MaxMessageTermination(1)
        )
        
        frontend_result = await frontend_team.run(task=frontend_task)
        frontend_srd = frontend_result.messages[-1].content
        
        # Step 3: Generate backend SRD
        backend_prompt = f"""
        BACKEND SPECIALIST TASK: Create a detailed Backend SRD document.

        CRITICAL INSTRUCTIONS:
        - Focus ONLY on server-side, database, and system architecture requirements
        - DO NOT include frontend, UI, or client-side implementation details
        - Extract ONLY backend-related requirements from the analysis below

        REQUIREMENTS ANALYSIS:
        {analysis_content}

        DELIVERABLE: Create a comprehensive Backend Software Requirements Document that focuses exclusively on:
        1. Server architecture and system design patterns
        2. Database design, schemas, and data models
        3. API specifications and web service definitions
        4. Business logic and server-side algorithms
        5. Authentication, authorization, and security systems
        6. Performance, scalability, and infrastructure requirements
        7. Integration with external services and third-party APIs
        8. DevOps, deployment, and monitoring requirements

        Generate a professional SRD document in markdown format with detailed backend specifications.
        """
        
        backend_task = TextMessage(content=backend_prompt, source="user")
        backend_team = RoundRobinGroupChat(
            participants=[self.backend_agent],
            termination_condition=MaxMessageTermination(1)
        )
        
        backend_result = await backend_team.run(task=backend_task)
        backend_srd = backend_result.messages[-1].content
        
        return {
            "frontend_srd": frontend_srd,
            "backend_srd": backend_srd,
            "analysis": analysis_content
        }
    
    async def save_srds(self, srd_content: Dict[str, str], output_dir: str = "output") -> Tuple[str, str]:
        """
        Save the generated SRDs to markdown files
        
        Args:
            srd_content: Dictionary containing SRD content
            output_dir: Directory to save the files
            
        Returns:
            Tuple of (frontend_file_path, backend_file_path)
        """
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Save frontend SRD
        frontend_path = os.path.join(output_dir, "srd_frontend.md")
        with open(frontend_path, 'w', encoding='utf-8') as f:
            f.write(srd_content["frontend_srd"])
        
        # Save backend SRD
        backend_path = os.path.join(output_dir, "srd_backend.md")
        with open(backend_path, 'w', encoding='utf-8') as f:
            f.write(srd_content["backend_srd"])
        
        return frontend_path, backend_path