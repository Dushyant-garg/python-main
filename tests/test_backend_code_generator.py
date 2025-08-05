"""
Tests for BackendCodeGenerator agent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.backend_code_generator import BackendCodeGenerator


class TestBackendCodeGenerator:
    """Test suite for BackendCodeGenerator"""
    
    @pytest.fixture
    def generator(self, environment_vars):
        """Create BackendCodeGenerator instance for testing"""
        with patch('app.agents.backend_code_generator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return BackendCodeGenerator()
    
    @pytest.mark.unit
    def test_init(self, generator):
        """Test BackendCodeGenerator initialization"""
        assert generator is not None
        assert hasattr(generator, 'api_designer_agent')
        assert hasattr(generator, 'model_developer_agent')
        assert hasattr(generator, 'business_logic_agent')
        assert hasattr(generator, 'integration_agent')
        assert hasattr(generator, 'database_migration_agent')
        assert hasattr(generator, 'code_coordinator_agent')
    
    @pytest.mark.unit
    def test_system_messages(self, generator):
        """Test that all agent system messages are properly defined"""
        messages = {
            'api_designer': generator._get_api_designer_system_message(),
            'model_developer': generator._get_model_developer_system_message(),
            'business_logic': generator._get_business_logic_system_message(),
            'integration': generator._get_integration_system_message(),
            'database_migration': generator._get_database_migration_system_message(),
            'code_coordinator': generator._get_code_coordinator_system_message()
        }
        
        for agent_name, message in messages.items():
            assert len(message) > 100, f"{agent_name} message too short"
            assert "RESPONSIBILITIES" in message, f"{agent_name} missing responsibilities"
            assert "CRITICAL GUIDELINES" in message, f"{agent_name} missing guidelines"
            assert "OUTPUT FORMAT" in message, f"{agent_name} missing output format"
    
    @pytest.mark.unit
    def test_api_designer_message_content(self, generator):
        """Test APIDesigner system message contains required elements"""
        message = generator._get_api_designer_system_message()
        
        required_terms = [
            "APIDesignerAgent", "FastAPI", "RESTful", "endpoints", 
            "Pydantic", "HTTP methods", "authentication", "error handling"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.unit
    def test_model_developer_message_content(self, generator):
        """Test ModelDeveloper system message contains required elements"""
        message = generator._get_model_developer_system_message()
        
        required_terms = [
            "ModelDeveloperAgent", "SQLAlchemy", "Pydantic", "database", 
            "models", "relationships", "constraints", "validation"
        ]
        
        for term in required_terms:
            assert term in message, f"Missing required term: {term}"
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_backend_code_success(self, generator, sample_backend_srd):
        """Test successful backend code generation"""
        with patch('app.agents.backend_code_generator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock conversation with code generation
            mock_messages = [
                Mock(content="""
# main.py
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
""", source="APIDesignerAgent"),
                Mock(content="""
# models.py
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```
""", source="ModelDeveloperAgent"),
                Mock(content="""
# requirements.txt
```
fastapi==0.116.1
uvicorn==0.32.1
sqlalchemy==2.0.23
```
""", source="CodeCoordinatorAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            result = await generator.generate_backend_code(sample_backend_srd, "test_project")
            
            assert result is not None
            assert isinstance(result, dict)
            assert len(result) > 0
            
            # Check that code files were generated
            python_files = [f for f in result.keys() if f.endswith('.py')]
            assert len(python_files) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_backend_code_empty_srd(self, generator):
        """Test code generation with empty SRD"""
        with pytest.raises(ValueError):
            await generator.generate_backend_code("", "test_project")
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_generate_backend_code_error_handling(self, generator, sample_backend_srd):
        """Test error handling in code generation"""
        with patch('app.agents.backend_code_generator.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            mock_instance.run.side_effect = Exception("Test error")
            
            result = await generator.generate_backend_code(sample_backend_srd, "test_project")
            
            assert result is not None
            assert "error" in result
    
    @pytest.mark.unit
    def test_extract_generated_code(self, generator):
        """Test code extraction from conversation messages"""
        messages = [
            Mock(content="""
# main.py
```python
from fastapi import FastAPI
app = FastAPI()
```

# models.py  
```python
from sqlalchemy import Column, Integer
```
""", source="TestAgent")
        ]
        
        result = generator._extract_generated_code(messages, "test_project")
        
        assert isinstance(result, dict)
        assert len(result) > 0
    
    @pytest.mark.unit
    def test_fallback_structure_creation(self, generator):
        """Test fallback structure when no code is extracted"""
        messages = [Mock(content="No code blocks here", source="TestAgent")]
        
        result = generator._create_fallback_structure(messages, "test_project")
        
        assert isinstance(result, dict)
        assert any("test_project" in path for path in result.keys())
        assert any(path.endswith('.py') for path in result.keys())
        assert any(path.endswith('.txt') for path in result.keys())
        assert any(path.endswith('.md') for path in result.keys())
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_generated_code(self, generator, temp_output_dir, mock_generated_code):
        """Test saving generated code to disk"""
        project_path = await generator.save_generated_code(mock_generated_code, temp_output_dir)
        
        assert project_path is not None
        assert temp_output_dir in project_path
    
    @pytest.mark.unit
    def test_code_extraction_patterns(self, generator):
        """Test various code block patterns are extracted correctly"""
        test_patterns = [
            # Standard Python code block
            """```python
def hello():
    return "world"
```""",
            # File path comment
            """# app/main.py
```python
from fastapi import FastAPI
```""",
            # Multiple code blocks
            """# models.py
```python
class User:
    pass
```

# schemas.py
```python  
class UserSchema:
    pass
```"""
        ]
        
        for pattern in test_patterns:
            messages = [Mock(content=pattern, source="TestAgent")]
            result = generator._extract_generated_code(messages, "test")
            assert len(result) > 0, f"Failed to extract from pattern: {pattern[:50]}..."


class TestBackendAgentMessages:
    """Test individual agent system messages for backend code generation"""
    
    @pytest.fixture
    def generator(self, environment_vars):
        """Create generator for message testing"""
        with patch('app.agents.backend_code_generator.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return BackendCodeGenerator()
    
    @pytest.mark.unit
    def test_api_designer_specialization(self, generator):
        """Test APIDesigner message focuses on API design"""
        message = generator._get_api_designer_system_message()
        
        # Should focus on API design, not other concerns
        assert "API" in message
        assert "endpoint" in message.lower()
        assert "FastAPI" in message
        assert "Do not implement business logic" in message or "Focus EXCLUSIVELY on API design" in message
    
    @pytest.mark.unit
    def test_model_developer_specialization(self, generator):
        """Test ModelDeveloper message focuses on data modeling"""
        message = generator._get_model_developer_system_message()
        
        assert "model" in message.lower()
        assert "SQLAlchemy" in message
        assert "database" in message.lower()
        assert "Do not implement API endpoints" in message or "Focus EXCLUSIVELY on data models" in message
    
    @pytest.mark.unit
    def test_business_logic_specialization(self, generator):
        """Test BusinessLogic message focuses on business rules"""
        message = generator._get_business_logic_system_message()
        
        assert "business" in message.lower()
        assert "service" in message.lower()
        assert "logic" in message.lower()
        assert "Do not implement API endpoints" in message or "Focus EXCLUSIVELY on business logic" in message
    
    @pytest.mark.unit
    def test_integration_specialization(self, generator):
        """Test Integration message focuses on external services"""
        message = generator._get_integration_system_message()
        
        assert "integration" in message.lower()
        assert "external" in message.lower()
        assert "API" in message
        assert "Do not implement core business logic" in message or "Focus EXCLUSIVELY on external integrations" in message
    
    @pytest.mark.unit
    def test_database_migration_specialization(self, generator):
        """Test DatabaseMigration message focuses on DB setup"""
        message = generator._get_database_migration_system_message()
        
        assert "migration" in message.lower()
        assert "database" in message.lower()
        assert "Alembic" in message
        assert "Do not implement business logic" in message or "Focus EXCLUSIVELY on database setup" in message
    
    @pytest.mark.unit
    def test_code_coordinator_orchestration(self, generator):
        """Test CodeCoordinator message focuses on overall coordination"""
        message = generator._get_code_coordinator_system_message()
        
        assert "coordinator" in message.lower() or "orchestrat" in message.lower()
        assert "project" in message.lower()
        assert "integration" in message.lower()
        assert "TEAM WORKFLOW" in message


class TestBackendCodeGeneratorIntegration:
    """Integration tests for BackendCodeGenerator"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_complete_backend_generation_workflow(self, environment_vars, sample_backend_srd, temp_output_dir):
        """Test complete backend code generation workflow"""
        with patch('app.agents.backend_code_generator.OpenAIChatCompletionClient') as mock_client, \
             patch('app.agents.backend_code_generator.RoundRobinGroupChat') as mock_chat:
            
            # Setup mocks
            mock_client.return_value = Mock()
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Create comprehensive mock conversation
            mock_messages = [
                # API Designer output
                Mock(content="""
# app/main.py
```python
from fastapi import FastAPI, Depends, HTTPException
from app.routers import users, tasks

app = FastAPI(title="Task Management API")
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
```

# app/routers/users.py
```python
from fastapi import APIRouter, Depends
from app.schemas import UserCreate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {"id": 1, "email": user.email}
```
""", source="APIDesignerAgent"),
                
                # Model Developer output
                Mock(content="""
# app/models.py
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
```

# app/schemas.py
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
```
""", source="ModelDeveloperAgent"),
                
                # Business Logic output
                Mock(content="""
# app/services/user_service.py
```python
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        user = User(email=user_data.email)
        self.db.add(user)
        self.db.commit()
        return user
```
""", source="BusinessLogicAgent"),
                
                # Database Migration output
                Mock(content="""
# alembic/versions/001_initial.py
```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```
""", source="DatabaseMigrationAgent"),
                
                # Code Coordinator output
                Mock(content="""
# requirements.txt
```
fastapi==0.116.1
uvicorn[standard]==0.32.1
sqlalchemy==2.0.23
alembic==1.13.1
pydantic==2.10.4
```

# README.md
```markdown
# Task Management Backend

FastAPI-based backend for task management system.

## Setup

pip install -r requirements.txt
uvicorn app.main:app --reload
```
""", source="CodeCoordinatorAgent")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            # Create generator and run complete workflow
            generator = BackendCodeGenerator()
            
            # Step 1: Generate code
            generated_files = await generator.generate_backend_code(sample_backend_srd, "task_management_backend")
            
            assert generated_files is not None
            assert isinstance(generated_files, dict)
            assert len(generated_files) > 0
            
            # Verify file types
            python_files = [f for f in generated_files.keys() if f.endswith('.py')]
            config_files = [f for f in generated_files.keys() if f.endswith('.txt') or f.endswith('.md')]
            
            assert len(python_files) > 0, "Should generate Python files"
            assert len(config_files) > 0, "Should generate configuration files"
            
            # Step 2: Save code to disk
            project_path = await generator.save_generated_code(generated_files, temp_output_dir)
            
            assert project_path is not None
            assert temp_output_dir in project_path
            
            # Verify content quality
            main_py_files = [f for f in generated_files.keys() if 'main.py' in f]
            if main_py_files:
                main_content = generated_files[main_py_files[0]]
                assert "FastAPI" in main_content
                assert "app =" in main_content
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_backend_generation_performance(self, environment_vars, sample_backend_srd):
        """Test backend generation performance"""
        import time
        
        with patch('app.agents.backend_code_generator.OpenAIChatCompletionClient') as mock_client, \
             patch('app.agents.backend_code_generator.RoundRobinGroupChat') as mock_chat:
            
            mock_client.return_value = Mock()
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock quick response
            mock_result = Mock()
            mock_result.messages = [Mock(content="# Quick backend code", source="TestAgent")]
            mock_instance.run.return_value = mock_result
            
            generator = BackendCodeGenerator()
            
            start_time = time.time()
            await generator.generate_backend_code(sample_backend_srd, "perf_test")
            end_time = time.time()
            
            # Should complete quickly with mocked responses
            assert end_time - start_time < 2.0  # Less than 2 seconds