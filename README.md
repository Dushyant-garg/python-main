# Requirements Analyzer

A FastAPI application that uses AutoGen and OpenAI to analyze project documents and generate Software Requirements Documents (SRDs) for both frontend and backend development.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **AI-Powered Analysis**: Uses AutoGen agents with OpenAI LLM for intelligent requirement extraction
- **Dual SRD Generation**: Automatically generates separate SRDs for frontend and backend
- **🔄 Feedback & Regeneration**: UserProxy agent processes user feedback to improve SRDs
- **RESTful API**: Clean API endpoints for integration
- **Structured Output**: Well-formatted Markdown SRDs
- **🎨 Streamlit UI**: Simple web interface for reviewing and approving SRDs
- **✅ Interactive Workflow**: Accept or Reject buttons with feedback integration

## Architecture

The application consists of:

1. **Document Parser**: Extracts text from uploaded documents
2. **RequirementAnalyzer Agent**: AutoGen 0.10.0-based multi-agent system that:
   - Uses specialized agents for analysis (RequirementAnalyst, FrontendSpecialist, BackendSpecialist)
   - Includes UserProxy agent for processing feedback and coordinating regeneration
   - Leverages OpenAI's latest models through AutoGen's modern API
   - Generates comprehensive frontend and backend SRDs
3. **FastAPI Backend**: RESTful API with latest FastAPI 0.116.1 for document upload and analysis

### Key Technologies:
- **AutoGen 0.10.0**: Latest multi-agent conversation framework
- **OpenAI 1.58.1**: Latest OpenAI API integration
- **FastAPI 0.116.1**: Modern, fast web framework
- **Pydantic 2.10.4**: Advanced data validation

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
python setup.py
```
This will automatically install compatible versions and set up the environment.

#### Option 2: Manual Setup
1. Clone the repository and navigate to the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   ```

#### Troubleshooting
If you encounter dependency or import errors:
1. Run the automated setup: `python setup.py`
2. Or manually fix version conflicts:
   ```bash
   pip uninstall openai pyautogen autogen autogen-agentchat autogen-ext
   pip install pyautogen==0.10.0 autogen-agentchat==0.7.1 autogen-ext[openai]==0.7.1 openai==1.58.1
   ```

### Running the Application

#### Option 1: Full Stack (UI + API)
Run both FastAPI backend and Streamlit UI:
```bash
python run_ui.py
```

This will start:
- 🔗 FastAPI Backend: http://localhost:8000
- 🎨 Streamlit UI: http://localhost:8501

#### Option 2: API Only
Start just the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### 1. Upload Document
```http
POST /upload-document
```
Upload a document for analysis. Returns file path and text preview.

### 2. Analyze Requirements
```http
POST /analyze-requirements
```
Analyze an uploaded document and generate SRDs.

### 3. Combined Upload and Analysis
```http
POST /analyze-from-upload
```
Upload and analyze a document in one step.

### 4. Get SRD Content
```http
GET /srd-content/{file_type}?output_dir=output
```
Retrieve generated SRD content (frontend or backend).

### 5. Regenerate SRD with Feedback
```http
POST /regenerate-srd
```
Regenerate a specific SRD based on user feedback using the UserProxy agent.

## Usage Examples

### 🎨 Streamlit UI (Recommended)

1. **Start the application:**
   ```bash
   python run_ui.py
   ```

2. **Open your browser:**
   Go to `http://localhost:8501`

3. **Upload and review:**
   - Upload a requirements document (PDF, DOCX, TXT)
   - Click "Analyze Document"
   - Review generated Frontend and Backend SRDs
   - Click "Accept" to approve or "Reject" to provide feedback

4. **Feedback workflow (when rejecting):**
   - Provide specific feedback in the text area
   - Click "Regenerate" to get improved SRD using UserProxy agent
   - Review the updated SRD and accept/reject again

### 🔗 API Usage

1. **Upload a Document**:
   ```bash
   curl -X POST "http://localhost:8000/upload-document" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@project_requirements.pdf"
   ```

2. **Analyze and Generate SRDs**:
   ```bash
   curl -X POST "http://localhost:8000/analyze-requirements" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "file_path": "uploads/project_requirements.pdf",
          "output_directory": "output"
        }'
   ```

3. **Or do both in one step**:
   ```bash
   curl -X POST "http://localhost:8000/analyze-from-upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@project_requirements.pdf" \
        -F "output_directory=output"
   ```

## Generated SRDs

The application generates two detailed SRDs:

- **`srd_frontend.md`**: Frontend requirements including UI/UX, user interactions, responsive design, and client-side architecture
- **`srd_backend.md`**: Backend requirements including APIs, data models, business logic, security, and infrastructure

## Project Structure

```
agents/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── document_parser.py   # Document parsing logic
│   └── agents/
│       ├── __init__.py
│       └── requirement_analyzer.py  # AutoGen agent system
├── streamlit_ui.py          # Streamlit web interface
├── run_ui.py               # Startup script for UI + API
├── test_ui.py              # UI testing script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── uploads/               # Uploaded documents (created automatically)
└── output/                # Generated SRDs (created automatically)
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4)

## Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Missing files
- Empty documents
- OpenAI API errors
- File system errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.