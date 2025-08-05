#!/usr/bin/env python3
"""
Test script to demonstrate the RequirementAnalyzer functionality
"""

import asyncio
import os
from pathlib import Path
from app.document_parser import DocumentParser
from app.agents.requirement_analyzer import RequirementAnalyzer

async def test_requirement_analyzer():
    """Test the RequirementAnalyzer with sample text"""
    
    # Sample project requirements text
    sample_text = """
    Project: Task Management System
    
    We need to build a web-based task management application that allows teams to collaborate effectively.
    
    Key Features:
    - User authentication and authorization
    - Project creation and management
    - Task creation, assignment, and tracking
    - Real-time notifications
    - File attachments
    - Comment system
    - Dashboard with analytics
    - Mobile responsive design
    
    Technical Requirements:
    - Frontend: React.js with TypeScript
    - Backend: Python FastAPI
    - Database: PostgreSQL
    - Authentication: JWT tokens
    - Real-time features: WebSockets
    - File storage: AWS S3
    - Deployment: Docker containers
    
    Performance: Support 500+ concurrent users with sub-second response times.
    Security: HTTPS, data encryption, secure authentication.
    """
    
    print("🧪 Testing RequirementAnalyzer...")
    print("=" * 50)
    
    try:
        # Initialize the analyzer
        analyzer = RequirementAnalyzer()
        print("✓ RequirementAnalyzer initialized")
        
        # Analyze the sample requirements
        print("🔍 Analyzing requirements...")
        print("⚠️  Note: This may take a few minutes as it uses the latest AutoGen API...")
        results = await analyzer.analyze_requirements(sample_text)
        
        # Save the results
        print("💾 Saving SRDs...")
        frontend_path, backend_path = await analyzer.save_srds(results, "test_output")
        
        print("✅ Analysis completed successfully!")
        print(f"📄 Frontend SRD saved to: {frontend_path}")
        print(f"📄 Backend SRD saved to: {backend_path}")
        
        # Show a preview of the analysis
        print("\n" + "=" * 50)
        print("📊 ANALYSIS PREVIEW:")
        print("=" * 50)
        analysis_preview = results["analysis"][:500] + "..." if len(results["analysis"]) > 500 else results["analysis"]
        print(analysis_preview)
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set the OPENAI_API_KEY environment variable")
        print("2. Installed all required dependencies with latest versions")
        print("3. Run: python fix_dependencies.py")

async def test_document_parser():
    """Test the DocumentParser with the example file"""
    
    print("\n🧪 Testing DocumentParser...")
    print("=" * 50)
    
    example_file = "example_project_requirements.md"
    
    if os.path.exists(example_file):
        try:
            parser = DocumentParser()
            text = await parser.parse_document(example_file)
            
            print("✓ Document parsed successfully")
            print(f"📄 Extracted {len(text)} characters")
            print(f"📝 Preview: {text[:200]}...")
            
            return text
            
        except Exception as e:
            print(f"❌ Error parsing document: {str(e)}")
    else:
        print(f"⚠️  Example file not found: {example_file}")
    
    return None

async def main():
    """Main test function"""
    print("🚀 Requirements Analyzer Test Suite")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Create test output directory
    Path("test_output").mkdir(exist_ok=True)
    
    # Test document parser
    parsed_text = await test_document_parser()
    
    # Test requirement analyzer
    await test_requirement_analyzer()
    
    # If we have parsed text from the example file, analyze it too
    if parsed_text:
        print("\n🔍 Analyzing example project requirements...")
        try:
            analyzer = RequirementAnalyzer()
            results = await analyzer.analyze_requirements(parsed_text)
            frontend_path, backend_path = await analyzer.save_srds(results, "test_output")
            
            print("✅ Example analysis completed!")
            print(f"📄 Files saved: {frontend_path}, {backend_path}")
            
        except Exception as e:
            print(f"❌ Error analyzing example: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())