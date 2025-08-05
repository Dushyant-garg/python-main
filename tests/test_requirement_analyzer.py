"""
Tests for RequirementAnalyzer agent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.requirement_analyzer import RequirementAnalyzer


class TestRequirementAnalyzer:
    """Test suite for RequirementAnalyzer"""
    
    @pytest.fixture
    def analyzer(self, environment_vars):
        """Create RequirementAnalyzer instance for testing"""
        with patch('app.agents.requirement_analyzer.OpenAIChatCompletionClient') as mock_client:
            mock_client.return_value = Mock()
            return RequirementAnalyzer()
    
    @pytest.mark.unit
    def test_init(self, analyzer):
        """Test RequirementAnalyzer initialization"""
        assert analyzer is not None
        assert hasattr(analyzer, 'analyst_agent')
        assert hasattr(analyzer, 'frontend_agent')
        assert hasattr(analyzer, 'backend_agent')
        assert hasattr(analyzer, 'user_proxy_agent')
    
    @pytest.mark.unit
    def test_system_messages(self, analyzer):
        """Test that system messages are properly defined"""
        analyst_msg = analyzer._get_analyst_system_message()
        frontend_msg = analyzer._get_frontend_system_message()
        backend_msg = analyzer._get_backend_system_message()
        user_proxy_msg = analyzer._get_user_proxy_system_message()
        
        # Check that messages are not empty and contain key terms
        assert len(analyst_msg) > 100
        assert "RequirementAnalyst" in analyst_msg
        assert "categoriz" in analyst_msg.lower()
        
        assert len(frontend_msg) > 100
        assert "Frontend" in frontend_msg
        assert "component" in frontend_msg.lower()
        
        assert len(backend_msg) > 100
        assert "Backend" in backend_msg
        assert "database" in backend_msg.lower()
        
        assert len(user_proxy_msg) > 100
        assert "UserProxy" in user_proxy_msg
        assert "feedback" in user_proxy_msg.lower()
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_analyze_requirements_success(self, analyzer, sample_document_text, mock_agent_conversation):
        """Test successful requirement analysis"""
        # Mock the RoundRobinGroupChat
        with patch('app.agents.requirement_analyzer.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Create mock result with conversation messages
            mock_result = Mock()
            mock_result.messages = mock_agent_conversation
            mock_instance.run.return_value = mock_result
            
            # Run analysis
            result = await analyzer.analyze_requirements(sample_document_text)
            
            # Verify results
            assert result is not None
            assert "frontend_srd" in result
            assert "backend_srd" in result
            assert "analysis" in result
            
            # Check content quality
            assert len(result["frontend_srd"]) > 50
            assert len(result["backend_srd"]) > 50
            assert "Frontend" in result["frontend_srd"]
            assert "Backend" in result["backend_srd"]
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_analyze_requirements_empty_text(self, analyzer):
        """Test analysis with empty text"""
        with pytest.raises(ValueError):
            await analyzer.analyze_requirements("")
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_analyze_requirements_error_handling(self, analyzer, sample_document_text):
        """Test error handling in analysis"""
        with patch('app.agents.requirement_analyzer.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            mock_instance.run.side_effect = Exception("Test error")
            
            result = await analyzer.analyze_requirements(sample_document_text)
            
            # Should return error information
            assert result is not None
            assert "error" in str(result).lower()
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_regenerate_srd_with_feedback(self, analyzer):
        """Test SRD regeneration with user feedback"""
        feedback = "Please add more details about authentication"
        srd_type = "frontend"
        original_analysis = "Basic task management requirements"
        
        with patch('app.agents.requirement_analyzer.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock improved response
            mock_message = Mock()
            mock_message.content = "# Improved Frontend SRD\n## Enhanced Authentication\nDetailed auth requirements..."
            mock_message.source = "FrontendSpecialist"
            
            mock_result = Mock()
            mock_result.messages = [mock_message]
            mock_instance.run.return_value = mock_result
            
            result = await analyzer.regenerate_srd_with_feedback(srd_type, feedback, original_analysis)
            
            assert result is not None
            assert "frontend_srd" in result
            assert len(result["frontend_srd"]) > 50
            assert "Enhanced Authentication" in result["frontend_srd"]
    
    @pytest.mark.unit
    def test_extract_srd_content(self, analyzer, mock_agent_conversation):
        """Test SRD content extraction from messages"""
        result = analyzer._extract_srd_content(mock_agent_conversation)
        
        assert "frontend_srd" in result
        assert "backend_srd" in result
        assert "analysis" in result
        
        # Check that content was properly extracted
        assert "Frontend Software Requirements" in result["frontend_srd"]
        assert "Backend Software Requirements" in result["backend_srd"]
        assert "ANALYSIS COMPLETE" in result["analysis"]
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_srds(self, analyzer, temp_output_dir):
        """Test saving SRDs to files"""
        srd_content = {
            "frontend_srd": "# Frontend SRD\nTest frontend content",
            "backend_srd": "# Backend SRD\nTest backend content"
        }
        
        frontend_path, backend_path = await analyzer.save_srds(srd_content, temp_output_dir)
        
        # Check that paths are returned
        assert frontend_path.endswith("srd_frontend.md")
        assert backend_path.endswith("srd_backend.md")
        
        # Check that files would be created (mocked in conftest)
        assert temp_output_dir in frontend_path
        assert temp_output_dir in backend_path
    
    @pytest.mark.unit
    def test_message_extraction_robustness(self, analyzer):
        """Test extraction with various message formats"""
        # Test with minimal messages
        minimal_messages = [
            Mock(content="Frontend: basic UI", source="FrontendSpecialist"),
            Mock(content="Backend: basic API", source="BackendSpecialist")
        ]
        
        result = analyzer._extract_srd_content(minimal_messages)
        assert result["frontend_srd"] == "Frontend: basic UI"
        assert result["backend_srd"] == "Backend: basic API"
        
        # Test with no proper messages
        empty_messages = [Mock(content="Random content", source="UnknownAgent")]
        result = analyzer._extract_srd_content(empty_messages)
        assert result["frontend_srd"] == ""
        assert result["backend_srd"] == ""
    
    @pytest.mark.asyncio
    @pytest.mark.agent
    async def test_regeneration_error_handling(self, analyzer):
        """Test regeneration with invalid parameters"""
        # Test with invalid SRD type
        with pytest.raises(ValueError):
            await analyzer.regenerate_srd_with_feedback("invalid_type", "feedback", "analysis")
        
        # Test with empty feedback
        result = await analyzer.regenerate_srd_with_feedback("frontend", "", "analysis")
        assert "error" in str(result).lower()
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_analysis_performance(self, analyzer, sample_document_text):
        """Test that analysis completes within reasonable time"""
        import time
        
        with patch('app.agents.requirement_analyzer.RoundRobinGroupChat') as mock_chat:
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Mock quick response
            mock_result = Mock()
            mock_result.messages = [
                Mock(content="Quick frontend analysis", source="FrontendSpecialist"),
                Mock(content="Quick backend analysis", source="BackendSpecialist")
            ]
            mock_instance.run.return_value = mock_result
            
            start_time = time.time()
            await analyzer.analyze_requirements(sample_document_text)
            end_time = time.time()
            
            # Should complete quickly with mocked responses
            assert end_time - start_time < 1.0  # Less than 1 second
    
    @pytest.mark.unit
    def test_content_validation(self, analyzer):
        """Test content validation and filtering"""
        # Test with malformed content
        malformed_messages = [
            Mock(content="", source="FrontendSpecialist"),  # Empty content
            Mock(content=None, source="BackendSpecialist"),  # None content
            Mock(content="Valid content", source="RequirementAnalyst")
        ]
        
        # Should handle gracefully without errors
        result = analyzer._extract_srd_content(malformed_messages)
        assert isinstance(result, dict)
        assert "frontend_srd" in result
        assert "backend_srd" in result


class TestRequirementAnalyzerIntegration:
    """Integration tests for RequirementAnalyzer"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_full_workflow(self, environment_vars, sample_document_text, temp_output_dir):
        """Test complete analysis workflow"""
        with patch('app.agents.requirement_analyzer.OpenAIChatCompletionClient') as mock_client, \
             patch('app.agents.requirement_analyzer.RoundRobinGroupChat') as mock_chat:
            
            # Setup mocks
            mock_client.return_value = Mock()
            mock_instance = AsyncMock()
            mock_chat.return_value = mock_instance
            
            # Create realistic mock conversation
            mock_messages = [
                Mock(content="## Analysis: Frontend needs authentication, dashboard\n## Backend needs API, database", 
                     source="RequirementAnalyst"),
                Mock(content="# Frontend SRD\n## Authentication Module\nLogin/register forms\n## Dashboard\nTask overview", 
                     source="FrontendSpecialist"),
                Mock(content="# Backend SRD\n## API Endpoints\nREST API for tasks\n## Database\nPostgreSQL models", 
                     source="BackendSpecialist")
            ]
            
            mock_result = Mock()
            mock_result.messages = mock_messages
            mock_instance.run.return_value = mock_result
            
            # Create analyzer and run full workflow
            analyzer = RequirementAnalyzer()
            
            # Step 1: Analyze requirements
            analysis_result = await analyzer.analyze_requirements(sample_document_text)
            
            assert analysis_result is not None
            assert "frontend_srd" in analysis_result
            assert "backend_srd" in analysis_result
            
            # Step 2: Save SRDs
            frontend_path, backend_path = await analyzer.save_srds(analysis_result, temp_output_dir)
            
            assert frontend_path is not None
            assert backend_path is not None
            
            # Step 3: Test feedback regeneration
            feedback_result = await analyzer.regenerate_srd_with_feedback(
                "frontend", 
                "Add more authentication details", 
                analysis_result["analysis"]
            )
            
            assert feedback_result is not None
            assert "frontend_srd" in feedback_result