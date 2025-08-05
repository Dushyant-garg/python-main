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

Your responsibilities:
1. Analyze the provided document text thoroughly
2. Identify functional and non-functional requirements
3. Categorize requirements into frontend and backend components
4. Ensure requirements are specific, measurable, and testable
5. Extract user stories, business rules, and technical constraints

Focus on:
- User interface requirements (frontend)
- Business logic and data processing (backend)
- Integration requirements
- Performance and security considerations
- Technology stack preferences mentioned in the document

Provide a comprehensive analysis that will help frontend and backend specialists create detailed SRDs."""
    
    def _get_frontend_system_message(self) -> str:
        """Get system message for the frontend specialist"""
        return """You are a Frontend Architecture Specialist responsible for creating detailed Software Requirements Documents for frontend components.

Your task is to generate a comprehensive SRD for frontend development that includes:

## Frontend SRD Structure:
1. **Project Overview**
   - Purpose and scope of the frontend application
   - Target users and use cases

2. **Functional Requirements**
   - User interface requirements
   - User interaction flows
   - Form validations and inputs
   - Navigation structure
   - Content management

3. **Technical Requirements**
   - Technology stack (React, Vue, Angular, etc.)
   - Browser compatibility
   - Responsive design requirements
   - Accessibility standards (WCAG compliance)

4. **Design Requirements**
   - UI/UX guidelines
   - Visual design principles
   - Component library specifications
   - Theming and branding

5. **Performance Requirements**
   - Page load times
   - Bundle size constraints
   - SEO requirements

6. **Integration Requirements**
   - API endpoints to consume
   - Authentication integration
   - Third-party service integrations

7. **Testing Requirements**
   - Unit testing frameworks
   - E2E testing requirements
   - Cross-browser testing

Generate a detailed, professional SRD in Markdown format."""
    
    def _get_backend_system_message(self) -> str:
        """Get system message for the backend specialist"""
        return """You are a Backend Architecture Specialist responsible for creating detailed Software Requirements Documents for backend systems.

Your task is to generate a comprehensive SRD for backend development that includes:

## Backend SRD Structure:
1. **System Overview**
   - Purpose and scope of the backend system
   - High-level architecture
   - System boundaries

2. **Functional Requirements**
   - Business logic requirements
   - Data processing workflows
   - API specifications
   - Integration requirements

3. **Technical Requirements**
   - Technology stack (Python/FastAPI, Node.js, Java, etc.)
   - Database requirements (SQL/NoSQL)
   - Caching strategies
   - Message queues or event processing

4. **Data Requirements**
   - Data models and schemas
   - Data validation rules
   - Data migration requirements
   - Backup and recovery

5. **API Requirements**
   - RESTful API specifications
   - Authentication and authorization
   - Rate limiting and throttling
   - API versioning strategy

6. **Performance Requirements**
   - Response time requirements
   - Throughput expectations
   - Scalability requirements
   - Concurrent user support

7. **Security Requirements**
   - Authentication mechanisms
   - Authorization levels
   - Data encryption
   - Security compliance standards

8. **Infrastructure Requirements**
   - Deployment architecture
   - Monitoring and logging
   - DevOps and CI/CD requirements

Generate a detailed, professional SRD in Markdown format."""
    
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
        Please analyze the following project document and extract comprehensive requirements:

        {document_text}

        Provide a detailed analysis categorizing requirements into:
        1. Frontend requirements (UI, UX, user interactions)
        2. Backend requirements (business logic, data processing, APIs)
        3. Integration requirements
        4. Technical constraints and preferences
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
        Based on the following requirements analysis, generate a detailed Frontend Software Requirements Document (SRD):

        {analysis_content}

        Please create a comprehensive frontend SRD that covers all aspects of the user interface and user experience requirements.
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
        Based on the following requirements analysis, generate a detailed Backend Software Requirements Document (SRD):

        {analysis_content}

        Please create a comprehensive backend SRD that covers all aspects of the server-side architecture and business logic requirements.
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