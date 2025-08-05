# Testing Guide for Requirements Analyzer

This document provides comprehensive information about the testing strategy, setup, and execution for the Requirements Analyzer project.

## 📋 Table of Contents

- [Testing Strategy](#testing-strategy)
- [Test Categories](#test-categories)
- [Setup and Installation](#setup-and-installation)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## 🎯 Testing Strategy

Our testing strategy ensures reliability and quality across all components of the multi-agent system:

### Testing Pyramid

```
    🔺 Integration Tests (Few)
   🔸🔸 Agent Tests (Some)
  🔹🔹🔹 Unit Tests (Many)
 🔷🔷🔷🔷 API Tests (Foundation)
```

### Key Principles

1. **Comprehensive Coverage**: Target 80%+ code coverage
2. **Fast Feedback**: Unit tests run in <5 seconds
3. **Isolation**: Each test is independent and can run alone
4. **Mocking**: External dependencies (OpenAI API) are mocked
5. **Real Integration**: Integration tests verify component interaction

## 🏷️ Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and classes
- Fast execution (<1ms per test)
- High coverage of business logic
- Isolated with comprehensive mocking

**Example:**
```python
@pytest.mark.unit
def test_system_message_content(self, analyzer):
    """Test that system messages contain required elements"""
    message = analyzer._get_analyst_system_message()
    assert "RequirementAnalyst" in message
    assert len(message) > 100
```

### Agent Tests (`@pytest.mark.agent`)
- Test AI agent behavior and interactions
- Mock OpenAI API calls
- Verify agent conversation flow
- Test agent specialization

**Example:**
```python
@pytest.mark.agent
@pytest.mark.asyncio
async def test_analyze_requirements_success(self, analyzer, sample_srd):
    """Test successful requirement analysis"""
    with patch('app.agents.requirement_analyzer.RoundRobinGroupChat'):
        result = await analyzer.analyze_requirements(sample_srd)
        assert "frontend_srd" in result
```

### API Tests (`@pytest.mark.api`)
- Test FastAPI endpoints
- Validate request/response schemas
- Test error handling and validation
- End-to-end API workflow

**Example:**
```python
@pytest.mark.api
def test_upload_document_success(self, client):
    """Test successful document upload"""
    response = client.post("/upload-document", 
                          files={"file": ("test.txt", b"content", "text/plain")})
    assert response.status_code == 200
```

### Integration Tests (`@pytest.mark.integration`)
- Test component interaction
- File system operations
- Multi-agent workflows
- Real data flow (with mocked APIs)

**Example:**
```python
@pytest.mark.integration
async def test_complete_workflow(self, temp_dir):
    """Test complete analysis workflow"""
    # Test full pipeline from document to SRDs
```

### Performance Tests (`@pytest.mark.performance`)
- Test execution speed
- Memory usage validation
- Scalability testing
- Timeout handling

### Slow Tests (`@pytest.mark.slow`)
- Complex integration scenarios
- Large data processing
- Multi-step workflows
- May take >30 seconds

## 🛠️ Setup and Installation

### Prerequisites

```bash
# Python 3.9+ required
python --version

# Install project dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r requirements-test.txt
```

### Test Dependencies

- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Enhanced mocking
- **httpx**: HTTP client testing
- **respx**: HTTP mocking

### Environment Setup

```bash
# Set test environment variables
export OPENAI_API_KEY="test-api-key"
export OPENAI_MODEL="gpt-4"
export DATABASE_URL="sqlite:///test.db"
```

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests with coverage
python run_tests.py

# Or use pytest directly
python -m pytest tests/ --cov=app --cov-report=html -v
```

### Specific Test Categories

```bash
# Unit tests only (fast)
python run_tests.py unit

# Agent tests only
python run_tests.py agent

# API tests only
python run_tests.py api

# Integration tests only
python run_tests.py integration

# Performance tests
python run_tests.py performance

# Slow tests (may take time)
python run_tests.py slow
```

### Advanced Options

```bash
# Run tests in parallel
python -m pytest tests/ -n 4

# Run specific test file
python -m pytest tests/test_requirement_analyzer.py -v

# Run specific test function
python -m pytest tests/test_requirement_analyzer.py::TestRequirementAnalyzer::test_init -v

# Run tests with specific markers
python -m pytest tests/ -m "unit and not slow" -v

# Debug mode (stop on first failure)
python -m pytest tests/ -x -vvv
```

## 📊 Test Coverage

### Coverage Targets

- **Overall**: 80%+ coverage
- **Core Agents**: 90%+ coverage
- **API Endpoints**: 95%+ coverage
- **Critical Paths**: 100% coverage

### Coverage Reports

```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=app --cov-report=html

# View coverage in terminal
python -m pytest tests/ --cov=app --cov-report=term-missing

# Generate XML for CI
python -m pytest tests/ --cov=app --cov-report=xml
```

### Coverage Analysis

```bash
# Open HTML report
open htmlcov/index.html

# View specific file coverage
python -m coverage report app/agents/requirement_analyzer.py
```

## ✍️ Writing Tests

### Test File Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_requirement_analyzer.py
├── test_backend_code_generator.py
├── test_frontend_code_generator.py
├── test_integration_coordinator.py
├── test_api_endpoints.py
└── test_data/              # Test data files
```

### Test Class Organization

```python
class TestRequirementAnalyzer:
    """Main test class for RequirementAnalyzer"""
    
    @pytest.fixture
    def analyzer(self, environment_vars):
        """Create analyzer instance for testing"""
        return RequirementAnalyzer()
    
    @pytest.mark.unit
    def test_initialization(self, analyzer):
        """Test basic initialization"""
        pass
    
    @pytest.mark.agent
    @pytest.mark.asyncio
    async def test_analysis_workflow(self, analyzer):
        """Test agent workflow"""
        pass
```

### Fixture Guidelines

```python
# Use shared fixtures from conftest.py
def test_with_sample_data(self, sample_frontend_srd, temp_output_dir):
    """Test using shared fixtures"""
    pass

# Create specific fixtures when needed
@pytest.fixture
def custom_analyzer(self):
    """Custom analyzer configuration"""
    return RequirementAnalyzer(custom_config=True)
```

### Mocking Best Practices

```python
# Mock external dependencies
@patch('app.agents.requirement_analyzer.OpenAIChatCompletionClient')
def test_with_mocked_openai(self, mock_client):
    """Test with mocked OpenAI client"""
    mock_client.return_value = Mock()
    
# Use respx for HTTP mocking
@respx.mock
def test_http_calls(self):
    """Test HTTP calls with respx"""
    respx.get("http://api.example.com").mock(return_value=httpx.Response(200))
```

### Assertion Guidelines

```python
# Descriptive assertions
assert len(result) > 0, "Should generate at least one file"
assert "FastAPI" in content, "Generated code should contain FastAPI"

# Use pytest assertions for better error messages
with pytest.raises(ValueError, match="Invalid SRD type"):
    await analyzer.process_invalid_type()
```

## 🔄 Continuous Integration

### GitHub Actions Workflow

Our CI pipeline runs on:
- **Push**: to main/develop branches
- **Pull Request**: to main/develop branches
- **Schedule**: nightly full test suite

### CI Jobs

1. **Test Matrix**: Python 3.9, 3.10, 3.11 on Ubuntu
2. **Performance Tests**: Separate job for performance validation
3. **Security Scan**: Safety and Bandit security analysis
4. **Documentation**: API docs and README validation
5. **Compatibility**: Cross-platform testing (Ubuntu, Windows, macOS)

### CI Configuration

```yaml
# .github/workflows/test.yml
- name: Run all tests with coverage
  run: |
    python -m pytest tests/ --cov=app --cov-report=xml --cov-fail-under=70 -v
```

### CI Status Badges

Add to README.md:
```markdown
![Tests](https://github.com/username/repo/workflows/Test%20Suite/badge.svg)
![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Problem: ModuleNotFoundError
# Solution: Install in development mode
pip install -e .
```

#### 2. Async Test Issues
```python
# Problem: RuntimeWarning about unawaited coroutines
# Solution: Use @pytest.mark.asyncio
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
```

#### 3. Mock Configuration
```python
# Problem: Mock not working as expected
# Solution: Patch the exact import path
@patch('app.agents.requirement_analyzer.OpenAIChatCompletionClient')
def test_with_correct_mock(self, mock_client):
    pass
```

#### 4. File Path Issues
```python
# Problem: Files not found in tests
# Solution: Use temp directories
def test_file_operations(self, temp_output_dir):
    file_path = Path(temp_output_dir) / "test.txt"
```

#### 5. Environment Variables
```bash
# Problem: Missing environment variables
# Solution: Set in conftest.py or use environment_vars fixture
```

### Debug Mode

```bash
# Run tests with maximum verbosity
python -m pytest tests/ -vvv --tb=long

# Run with pdb debugger
python -m pytest tests/ --pdb

# Run single test with debugging
python -m pytest tests/test_requirement_analyzer.py::test_specific -vvv --pdb
```

### Performance Debugging

```bash
# Profile test execution
python -m pytest tests/ --profile

# Memory usage profiling
python -m pytest tests/ --memray
```

## 📈 Test Metrics

### Success Criteria

- ✅ All tests pass on Python 3.9, 3.10, 3.11
- ✅ Code coverage ≥ 80%
- ✅ No security vulnerabilities
- ✅ API documentation complete
- ✅ Cross-platform compatibility

### Quality Gates

1. **Code Coverage**: Minimum 80% overall
2. **Test Speed**: Unit tests < 5 seconds total
3. **No Flaky Tests**: 99.9% pass rate
4. **Security**: No high/medium vulnerabilities
5. **Documentation**: All public APIs documented

## 🤝 Contributing Tests

### Guidelines for New Tests

1. **Test First**: Write tests before implementation when possible
2. **One Assertion**: Focus each test on one specific behavior
3. **Clear Names**: Use descriptive test function names
4. **Proper Markers**: Tag tests with appropriate markers
5. **Mock External**: Always mock external dependencies
6. **Clean Up**: Use fixtures for setup/teardown

### Test Review Checklist

- [ ] Tests have clear, descriptive names
- [ ] Tests are properly categorized with markers
- [ ] External dependencies are mocked
- [ ] Assertions are specific and meaningful
- [ ] Tests clean up after themselves
- [ ] Coverage is maintained or improved
- [ ] Tests pass in CI environment

---

## 📞 Support

For testing questions or issues:

1. Check this documentation
2. Review existing test examples
3. Check CI logs for detailed error information
4. Create an issue with test failure details

**Happy Testing! 🧪✨**