"""
Backend Code Generator with Multiple Specialized Agents

This module implements a multi-agent system for generating backend code
based on Software Requirements Documents (SRDs).
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


class BackendCodeGenerator:
    """
    Multi-agent system for generating backend code from requirements
    """
    
    def __init__(self):
        """Initialize the BackendCodeGenerator with specialized agents"""
        
        # Initialize the OpenAI client
        self.model_client = OpenAIChatCompletionClient(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2,  # Slightly higher for code creativity
        )
        
        # Create specialized agents
        self.api_designer_agent = AssistantAgent(
            name="APIDesignerAgent",
            model_client=self.model_client,
            system_message=self._get_api_designer_system_message(),
        )
        
        self.model_developer_agent = AssistantAgent(
            name="ModelDeveloperAgent",
            model_client=self.model_client,
            system_message=self._get_model_developer_system_message(),
        )
        
        self.business_logic_agent = AssistantAgent(
            name="BusinessLogicAgent",
            model_client=self.model_client,
            system_message=self._get_business_logic_system_message(),
        )
        
        self.integration_agent = AssistantAgent(
            name="IntegrationAgent",
            model_client=self.model_client,
            system_message=self._get_integration_system_message(),
        )
        
        self.database_migration_agent = AssistantAgent(
            name="DatabaseMigrationAgent",
            model_client=self.model_client,
            system_message=self._get_database_migration_system_message(),
        )
        
        # Code coordinator agent
        self.code_coordinator_agent = AssistantAgent(
            name="CodeCoordinatorAgent",
            model_client=self.model_client,
            system_message=self._get_code_coordinator_system_message(),
        )
    
    def _get_api_designer_system_message(self) -> str:
        """Get system message for the API Designer agent"""
        return """You are the APIDesignerAgent, a specialist in designing RESTful APIs and endpoint architecture.

RESPONSIBILITIES:
1. Design API endpoints based on backend requirements
2. Define HTTP methods, routes, and request/response schemas
3. Create OpenAPI/Swagger specifications
4. Design authentication and authorization flows
5. Plan API versioning strategy

CRITICAL GUIDELINES:
- Follow RESTful principles and HTTP standards
- Use FastAPI with Pydantic models for type safety
- Include proper error handling and status codes
- Design consistent URL patterns and naming conventions
- Consider rate limiting and security measures

OUTPUT FORMAT:
Generate FastAPI endpoint definitions with:
- Route decorators and HTTP methods
- Pydantic request/response models
- Authentication decorators
- Error handling
- Comprehensive docstrings

EXAMPLE OUTPUT STRUCTURE:
```python
# API Endpoints
@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    \"\"\"Create a new user\"\"\"
    # Implementation details
```

Focus EXCLUSIVELY on API design and endpoints. Do not implement business logic or database operations.
"""

    def _get_model_developer_system_message(self) -> str:
        """Get system message for the Model Developer agent"""
        return """You are the ModelDeveloperAgent, a specialist in data modeling and database schema design.

RESPONSIBILITIES:
1. Design database models and schemas
2. Create Pydantic models for data validation
3. Define relationships between entities
4. Plan indexing strategies
5. Design data migration scripts

CRITICAL GUIDELINES:
- Use SQLAlchemy for ORM with proper relationships
- Create both database models and Pydantic schemas
- Follow database normalization principles
- Include proper constraints and validations
- Consider performance and scalability

OUTPUT FORMAT:
Generate SQLAlchemy models and Pydantic schemas:
- Database table definitions
- Model relationships (foreign keys, associations)
- Pydantic request/response models
- Database constraints and indexes
- Model validation rules

EXAMPLE OUTPUT STRUCTURE:
```python
# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    # ... other fields

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
```

Focus EXCLUSIVELY on data models and schemas. Do not implement API endpoints or business logic.
"""

    def _get_business_logic_system_message(self) -> str:
        """Get system message for the Business Logic agent"""
        return """You are the BusinessLogicAgent, a specialist in implementing core business functionality and application logic.

RESPONSIBILITIES:
1. Implement business rules and workflows
2. Create service layer functions
3. Handle data processing and transformations
4. Implement validation logic
5. Design error handling strategies

CRITICAL GUIDELINES:
- Separate business logic from API endpoints
- Use dependency injection patterns
- Implement proper error handling and logging
- Follow SOLID principles
- Create reusable service functions

OUTPUT FORMAT:
Generate service layer implementations:
- Business logic functions
- Data processing services
- Validation utilities
- Exception handling
- Background task implementations

EXAMPLE OUTPUT STRUCTURE:
```python
# Business Logic Services
class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        # Business logic implementation
```

Focus EXCLUSIVELY on business logic and services. Do not implement API endpoints or database models.
"""

    def _get_integration_system_message(self) -> str:
        """Get system message for the Integration agent"""
        return """You are the IntegrationAgent, a specialist in external service integrations and third-party API connections.

RESPONSIBILITIES:
1. Design external API integrations
2. Implement authentication with external services
3. Create webhook handlers
4. Design message queue integrations
5. Handle external service errors and retries

CRITICAL GUIDELINES:
- Use async HTTP clients (httpx, aiohttp)
- Implement proper retry mechanisms
- Handle rate limiting and timeouts
- Use environment variables for configuration
- Create mock services for testing

OUTPUT FORMAT:
Generate integration services:
- External API client classes
- Webhook handlers
- Queue message processors
- Configuration management
- Error handling and retry logic

EXAMPLE OUTPUT STRUCTURE:
```python
# External Service Integration
class PaymentServiceClient:
    def __init__(self, api_key: str, base_url: str):
        # Integration setup
        
    async def process_payment(self, payment_data: PaymentRequest):
        # External API integration
```

Focus EXCLUSIVELY on external integrations. Do not implement core business logic or database operations.
"""

    def _get_database_migration_system_message(self) -> str:
        """Get system message for the Database Migration agent"""
        return """You are the DatabaseMigrationAgent, a specialist in database setup, migrations, and data management.

RESPONSIBILITIES:
1. Create database migration scripts
2. Design database initialization procedures
3. Handle schema updates and versioning
4. Create seed data scripts
5. Plan backup and recovery strategies

CRITICAL GUIDELINES:
- Use Alembic for SQLAlchemy migrations
- Create idempotent migration scripts
- Include rollback procedures
- Handle data migrations safely
- Follow database best practices

OUTPUT FORMAT:
Generate migration and setup scripts:
- Alembic migration files
- Database initialization scripts
- Seed data creation
- Index creation scripts
- Database configuration

EXAMPLE OUTPUT STRUCTURE:
```python
# Alembic Migration
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        # ... migration details
    )

def downgrade():
    op.drop_table('users')
```

Focus EXCLUSIVELY on database setup and migrations. Do not implement business logic or API endpoints.
"""

    def _get_code_coordinator_system_message(self) -> str:
        """Get system message for the Code Coordinator agent"""
        return """You are the CodeCoordinatorAgent, responsible for orchestrating the code generation process and ensuring all components work together.

RESPONSIBILITIES:
1. Coordinate between all specialist agents
2. Ensure code consistency and integration
3. Create main application setup files
4. Generate project structure
5. Create documentation and README files

CRITICAL GUIDELINES:
- Ensure all generated code works together
- Create proper file organization
- Generate requirements.txt and configuration files
- Include proper imports and dependencies
- Create comprehensive documentation

OUTPUT FORMAT:
Generate project coordination files:
- Main application entry point
- Configuration management
- Dependency requirements
- Project structure documentation
- Integration instructions

TEAM WORKFLOW:
1. Analyze requirements document
2. Plan overall architecture
3. Coordinate with specialist agents
4. Integrate all generated components
5. Create final project structure
"""

    async def generate_backend_code(self, backend_srd: str, project_name: str = "generated_backend") -> Dict[str, str]:
        """
        Generate complete backend code from SRD using multi-agent collaboration
        
        Args:
            backend_srd: Backend Software Requirements Document content
            project_name: Name for the generated project
            
        Returns:
            Dictionary containing generated code files
        """
        
        # Create the initial task for code generation
        generation_task = f"""
BACKEND CODE GENERATION PROJECT

PROJECT NAME: {project_name}

BACKEND REQUIREMENTS DOCUMENT:
{backend_srd}

TEAM WORKFLOW:
1. CodeCoordinatorAgent: Analyze requirements and plan architecture
2. ModelDeveloperAgent: Design database models and schemas
3. APIDesignerAgent: Create API endpoints and routes
4. BusinessLogicAgent: Implement core business logic
5. IntegrationAgent: Handle external service integrations
6. DatabaseMigrationAgent: Create database setup and migrations
7. CodeCoordinatorAgent: Integrate all components and finalize

Each agent should focus on their specialty and create production-ready code.
The final output should be a complete, deployable FastAPI backend application.

BEGIN CODE GENERATION:
"""

        try:
            # Create the multi-agent team
            code_generation_team = RoundRobinGroupChat(
                participants=[
                    self.code_coordinator_agent,
                    self.model_developer_agent,
                    self.api_designer_agent,
                    self.business_logic_agent,
                    self.integration_agent,
                    self.database_migration_agent,
                    self.code_coordinator_agent  # Final coordination
                ],
                termination_condition=MaxMessageTermination(15)  # Allow comprehensive generation
            )
            
            # Start the code generation process
            task_message = TextMessage(content=generation_task, source="user")
            result = await code_generation_team.run(task=task_message)
            
            # Extract generated code from the conversation
            generated_files = self._extract_generated_code(result.messages, project_name)
            
            return generated_files
            
        except Exception as e:
            print(f"Error generating backend code: {str(e)}")
            return {"error": f"Code generation failed: {str(e)}"}
    
    def _extract_generated_code(self, messages: List, project_name: str) -> Dict[str, str]:
        """
        Extract generated code files from agent conversation messages
        
        Args:
            messages: List of conversation messages
            project_name: Name of the project
            
        Returns:
            Dictionary mapping file paths to code content
        """
        
        generated_files = {}
        current_file = None
        current_content = []
        
        for message in messages:
            if not hasattr(message, 'content'):
                continue
                
            content = message.content
            lines = content.split('\n')
            
            for line in lines:
                # Look for file indicators
                if line.strip().startswith('```python') or line.strip().startswith('```'):
                    if current_file and current_content:
                        # Save previous file
                        generated_files[current_file] = '\n'.join(current_content)
                        current_content = []
                    
                elif line.strip() == '```':
                    if current_file and current_content:
                        # End of code block
                        generated_files[current_file] = '\n'.join(current_content)
                        current_file = None
                        current_content = []
                        
                elif line.strip().startswith('#') and ('.' in line or '/' in line):
                    # Potential file path comment
                    potential_file = line.strip('#').strip()
                    if any(ext in potential_file for ext in ['.py', '.txt', '.md', '.yml', '.yaml']):
                        current_file = potential_file
                        
                elif current_file and line.strip():
                    # Add content to current file
                    current_content.append(line)
        
        # Handle any remaining content
        if current_file and current_content:
            generated_files[current_file] = '\n'.join(current_content)
        
        # If no files were extracted, create a comprehensive structure
        if not generated_files:
            generated_files = self._create_fallback_structure(messages, project_name)
        
        return generated_files
    
    def _create_fallback_structure(self, messages: List, project_name: str) -> Dict[str, str]:
        """Create a fallback file structure from conversation content"""
        
        # Combine all agent outputs
        all_content = []
        for message in messages:
            if hasattr(message, 'content') and hasattr(message, 'source'):
                agent_name = getattr(message, 'source', 'Unknown')
                all_content.append(f"# Generated by {agent_name}\n{message.content}\n\n")
        
        return {
            f"{project_name}/generated_code.py": '\n'.join(all_content),
            f"{project_name}/README.md": f"# {project_name}\n\nGenerated backend code from SRD analysis.",
            f"{project_name}/requirements.txt": "fastapi==0.116.1\nuvicorn[standard]==0.32.1\nsqlalchemy==2.0.23\nalembic==1.13.1\npydantic==2.10.4\n"
        }
    
    async def save_generated_code(self, generated_files: Dict[str, str], output_dir: str = "generated_code") -> str:
        """
        Save generated code files to disk
        
        Args:
            generated_files: Dictionary of file paths to content
            output_dir: Base directory for saving files
            
        Returns:
            Path to the saved project directory
        """
        
        base_path = Path(output_dir)
        base_path.mkdir(exist_ok=True)
        
        for file_path, content in generated_files.items():
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return str(base_path)