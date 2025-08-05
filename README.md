# Requirements Analyzer

A FastAPI application that uses AutoGen and OpenAI to analyze project documents and generate Software Requirements Documents (SRDs) for both frontend and backend development.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **AI-Powered Analysis**: Uses AutoGen agents with OpenAI LLM for intelligent requirement extraction
- **Dual SRD Generation**: Automatically generates separate SRDs for frontend and backend
- **RESTful API**: Clean API endpoints for integration
- **Structured Output**: Well-formatted Markdown SRDs

## Architecture

The application consists of:

1. **Document Parser**: Extracts text from uploaded documents
2. **RequirementAnalyzer Agent**: AutoGen-based multi-agent system that:
   - Analyzes project requirements
   - Generates frontend-specific SRD
   - Generates backend-specific SRD
3. **FastAPI Backend**: RESTful API for document upload and analysis

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

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

### Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

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

## Usage Example

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
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── uploads/                # Uploaded documents (created automatically)
└── output/                 # Generated SRDs (created automatically)
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