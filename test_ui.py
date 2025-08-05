#!/usr/bin/env python3
"""
Test script for the Streamlit UI
"""

import asyncio
import os
from app.agents.requirement_analyzer import RequirementAnalyzer

async def test_ui_workflow():
    """Test the complete UI workflow"""
    
    print("🧪 Testing Streamlit UI Workflow")
    print("=" * 40)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Sample requirements for testing
    sample_text = """
    Project: E-commerce Mobile App
    
    We need to build a mobile e-commerce application for iOS and Android.
    
    Frontend Requirements:
    - Product catalog with search and filtering
    - Shopping cart and checkout flow
    - User registration and login
    - Product reviews and ratings
    - Wishlist functionality
    - Push notifications for orders
    - Responsive design for tablets
    
    Backend Requirements:
    - User authentication and session management
    - Product inventory management
    - Order processing and payment integration
    - RESTful API for mobile app
    - Admin dashboard for managing products
    - Email notifications for orders
    - Analytics and reporting
    - Database design for users, products, orders
    """
    
    print("🤖 Testing AI agent analysis...")
    
    try:
        # Test the analyzer
        analyzer = RequirementAnalyzer()
        results = await analyzer.analyze_requirements(sample_text)
        
        # Check if we got results
        if results.get("frontend_srd") and results.get("backend_srd"):
            print("✅ AI analysis successful!")
            print(f"📄 Frontend SRD length: {len(results['frontend_srd'])} characters")
            print(f"📄 Backend SRD length: {len(results['backend_srd'])} characters")
            
            # Show previews
            print("\n📋 Frontend SRD Preview:")
            print("-" * 40)
            frontend_preview = results["frontend_srd"][:300] + "..." if len(results["frontend_srd"]) > 300 else results["frontend_srd"]
            print(frontend_preview)
            
            print("\n📋 Backend SRD Preview:")
            print("-" * 40)
            backend_preview = results["backend_srd"][:300] + "..." if len(results["backend_srd"]) > 300 else results["backend_srd"]
            print(backend_preview)
            
            print("\n✅ Test completed successfully!")
            print("\n🚀 Ready to test UI:")
            print("1. Run: python run_ui.py")
            print("2. Open: http://localhost:8501")
            print("3. Upload a document and test Accept/Reject buttons")
            
        else:
            print("❌ AI analysis failed - no SRDs generated")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check OPENAI_API_KEY")
        print("2. Run: python setup.py")
        print("3. Run: python fix_dependencies.py")

async def main():
    await test_ui_workflow()

if __name__ == "__main__":
    asyncio.run(main())