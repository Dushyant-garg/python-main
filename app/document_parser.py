import os
from pathlib import Path
from typing import Optional
import PyPDF2
from docx import Document
import aiofiles

class DocumentParser:
    """Parser for extracting text from various document formats"""
    
    @staticmethod
    async def parse_document(file_path: str) -> str:
        """
        Parse document and extract text content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return await DocumentParser._parse_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return await DocumentParser._parse_word(file_path)
        elif file_extension == '.txt':
            return await DocumentParser._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    async def _parse_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    async def _parse_word(file_path: str) -> str:
        """Extract text from Word document"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    @staticmethod
    async def _parse_text(file_path: str) -> str:
        """Read text file content"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            content = await file.read()
        return content.strip()