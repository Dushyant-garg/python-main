# Changelog

## v2.0.0 - Latest Versions Update (January 2025)

### 🚀 Major Updates

- **AutoGen 0.10.0**: Updated to the latest AutoGen with new agent architecture
- **OpenAI 1.58.1**: Latest OpenAI API integration
- **FastAPI 0.116.1**: Updated to the newest FastAPI version
- **Python 3.8+**: Modern Python support

### 🔧 Technical Changes

#### AutoGen Architecture Overhaul
- Migrated from legacy `autogen` to modern `autogen-agentchat` and `autogen-ext`
- Updated agent initialization using `OpenAIChatCompletionClient`
- Replaced old `UserProxyAgent` with `RoundRobinGroupChat` teams
- Implemented new `TextMessage` and `MaxMessageTermination` patterns

#### Dependency Updates
- `fastapi`: 0.104.1 → 0.116.1
- `uvicorn`: 0.24.0 → 0.32.1
- `python-multipart`: 0.0.6 → 0.0.18
- `pyautogen`: 0.2.25 → 0.10.0
- `openai`: 1.35.0 → 1.58.1
- `pydantic`: 2.5.0 → 2.10.4
- `aiofiles`: 23.2.0 → 24.1.0
- `PyPDF2`: 3.0.1 → 3.1.0
- `python-docx`: 1.1.0 → 1.1.2

#### New Packages Added
- `autogen-agentchat==0.7.1`: Core agent chat functionality
- `autogen-ext[openai]==0.7.1`: OpenAI integration extensions

### 🛠️ Setup Improvements

- Updated automated setup scripts for new dependency structure
- Enhanced conflict resolution in `fix_dependencies.py`
- Improved error messages and troubleshooting guidance
- Updated test suite for new AutoGen API

### 📚 Documentation Updates

- Updated README with latest installation instructions
- Added troubleshooting for new dependency structure
- Enhanced architecture documentation
- Updated API examples for new patterns

### 🔄 Migration Notes

**From v1.x to v2.0.0:**

1. **AutoGen API Changes**: The agent initialization and conversation patterns have completely changed
2. **Import Changes**: Replace `import autogen` with specific imports from `autogen_agentchat` and `autogen_ext`
3. **Configuration**: LLM config now uses `OpenAIChatCompletionClient` instead of config dictionaries
4. **Teams**: Conversations now use `RoundRobinGroupChat` instead of direct agent interactions

### 🏃‍♂️ Quick Migration

To update from previous versions:

```bash
# Option 1: Automated
python setup.py

# Option 2: Manual
python fix_dependencies.py

# Option 3: Clean install
pip uninstall openai pyautogen autogen autogen-agentchat autogen-ext
pip install -r requirements.txt
```

### 🚨 Breaking Changes

- **Agent API**: Complete rewrite of agent interaction patterns
- **Import Paths**: All AutoGen imports have changed
- **Configuration**: New model client initialization required
- **Message Format**: Different message handling in new API

---

## v1.0.0 - Initial Release

### Features
- Document parser for PDF, DOCX, TXT
- AutoGen-based requirement analysis
- Dual SRD generation (frontend/backend)
- FastAPI REST API
- Multi-format document support