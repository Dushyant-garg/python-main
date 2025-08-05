#!/usr/bin/env python3
"""
Test script to demonstrate the TRUE multi-agent RequirementAnalyzer functionality
"""

import asyncio
import os
from pathlib import Path
from app.document_parser import DocumentParser
from app.agents.requirement_analyzer import RequirementAnalyzer

async def test_multi_agent_collaboration():
    """Test the multi-agent RequirementAnalyzer with all three agents working together"""
    
    # E-commerce sample with clear frontend and backend distinctions
    sample_text = """
    Project: Online Bookstore Platform

    We need to build a comprehensive online bookstore where customers can browse, search, and purchase books.

    User Requirements:
    - Customers should be able to browse books by category, author, and genre
    - Search functionality with filters (price, rating, publication date)
    - User registration and login system
    - Shopping cart with add/remove functionality
    - Secure checkout process with multiple payment options
    - Order tracking and history
    - Book reviews and ratings system
    - Wishlist functionality
    - Responsive design for mobile and desktop
    - Admin panel for managing inventory

    Business Requirements:
    - Inventory management system
    - Order processing and fulfillment
    - Payment processing integration
    - Customer support system
    - Analytics and reporting
    - Email notifications for orders
    - Recommendation engine
    - Multi-language support

    Technical Requirements:
    - Frontend: React.js with TypeScript
    - Backend: Python FastAPI with PostgreSQL
    - Authentication: JWT with refresh tokens
    - Payment: Stripe and PayPal integration
    - File Storage: AWS S3 for book covers and documents
    - Search: Elasticsearch for advanced search
    - Caching: Redis for performance
    - Deployment: Docker on AWS ECS
    - Monitoring: CloudWatch and application logs
    """
    
    print("🤖 Testing TRUE Multi-Agent Collaboration...")
    print("=" * 70)
    print("Three agents will work together in sequence:")
    print("1. 📊 RequirementAnalyst - Analyzes and categorizes")
    print("2. 🎨 FrontendSpecialist - Creates frontend SRD")  
    print("3. ⚙️  BackendSpecialist - Creates backend SRD")
    print("=" * 70)
    
    try:
        # Initialize the analyzer
        analyzer = RequirementAnalyzer()
        print("✓ Multi-agent RequirementAnalyzer initialized")
        
        # Analyze with all three agents collaborating
        print("🔄 Starting multi-agent collaboration...")
        print("   This will show the actual conversation between agents...")
        results = await analyzer.analyze_requirements(sample_text)
        
        # Save the results
        print("💾 Saving agent-generated SRDs...")
        frontend_path, backend_path = await analyzer.save_srds(results, "test_output")
        
        print("✅ Multi-agent analysis completed!")
        print(f"📄 Frontend SRD: {frontend_path}")
        print(f"📄 Backend SRD: {backend_path}")
        
        # Show the full conversation to demonstrate agent collaboration
        if "full_conversation" in results:
            print("\n" + "=" * 70)
            print("💬 MULTI-AGENT CONVERSATION:")
            print("=" * 70)
            for i, message in enumerate(results["full_conversation"], 1):
                print(f"\n--- Message {i} ---")
                preview = message[:400] + "..." if len(message) > 400 else message
                print(preview)
        
        # Show individual outputs
        print("\n" + "=" * 70)
        print("📊 ANALYST'S CATEGORIZATION:")
        print("=" * 70)
        if results["analysis"]:
            analysis_preview = results["analysis"][:600] + "..." if len(results["analysis"]) > 600 else results["analysis"]
            print(analysis_preview)
        else:
            print("⚠️  No analysis content found")
        
        print("\n" + "=" * 70)
        print("🎨 FRONTEND SPECIALIST'S SRD:")
        print("=" * 70)
        if results["frontend_srd"]:
            frontend_preview = results["frontend_srd"][:600] + "..." if len(results["frontend_srd"]) > 600 else results["frontend_srd"]
            print(frontend_preview)
        else:
            print("⚠️  No frontend SRD content found")
        
        print("\n" + "=" * 70)
        print("⚙️  BACKEND SPECIALIST'S SRD:")
        print("=" * 70)
        if results["backend_srd"]:
            backend_preview = results["backend_srd"][:600] + "..." if len(results["backend_srd"]) > 600 else results["backend_srd"]
            print(backend_preview)
        else:
            print("⚠️  No backend SRD content found")
        
        # Verify agent collaboration
        print("\n" + "=" * 70)
        print("🔍 COLLABORATION VERIFICATION:")
        print("=" * 70)
        
        has_analysis = bool(results["analysis"])
        has_frontend = bool(results["frontend_srd"])
        has_backend = bool(results["backend_srd"])
        
        print(f"✓ Analyst provided categorization: {'Yes' if has_analysis else 'No'}")
        print(f"✓ Frontend specialist created SRD: {'Yes' if has_frontend else 'No'}")
        print(f"✓ Backend specialist created SRD: {'Yes' if has_backend else 'No'}")
        
        if has_analysis and has_frontend and has_backend:
            print("🎉 All three agents successfully collaborated!")
        else:
            print("⚠️  Some agents may not have contributed properly")
        
    except Exception as e:
        print(f"❌ Error during multi-agent testing: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set the OPENAI_API_KEY environment variable")
        print("2. Installed all required dependencies")
        print("3. Run: python setup.py")

async def main():
    """Main test function"""
    print("🚀 Multi-Agent Requirements Analyzer Test")
    print("Testing actual agent collaboration with AutoGen 0.10.0")
    print("=" * 70)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Create test output directory
    Path("test_output").mkdir(exist_ok=True)
    
    # Test multi-agent collaboration
    await test_multi_agent_collaboration()

if __name__ == "__main__":
    asyncio.run(main())