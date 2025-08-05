#!/usr/bin/env python3
"""
Test script to demonstrate the improved RequirementAnalyzer functionality
"""

import asyncio
import os
from pathlib import Path
from app.document_parser import DocumentParser
from app.agents.requirement_analyzer import RequirementAnalyzer

async def test_improved_analyzer():
    """Test the improved RequirementAnalyzer with sample text"""
    
    # More detailed sample project requirements text
    sample_text = """
    Project: E-Commerce Platform

    We need to build a comprehensive e-commerce platform for selling books online.

    Frontend Requirements:
    - User-friendly product catalog with search and filtering
    - Shopping cart functionality with add/remove items
    - User registration and login forms
    - Responsive design for mobile and desktop
    - Product review and rating system
    - Order history page for users
    - Payment form integration
    - Real-time stock availability updates
    - Interactive product image gallery
    - Wishlist functionality

    Backend Requirements:
    - User authentication and session management
    - Product inventory management system
    - Order processing and payment integration
    - Database design for users, products, orders
    - Email notification system
    - Admin panel for managing products
    - API endpoints for all frontend operations
    - Search engine with filtering capabilities
    - Inventory tracking and stock management
    - Payment gateway integration (Stripe/PayPal)
    - Order fulfillment and shipping integration

    Technical Requirements:
    - Frontend: React.js with Redux for state management
    - Backend: Python FastAPI with PostgreSQL database
    - Authentication: JWT tokens with refresh mechanism
    - Payment: Stripe payment processing
    - Deployment: Docker containers on AWS
    - File storage: AWS S3 for product images
    - Real-time features: WebSocket for stock updates
    - Performance: Support 1000+ concurrent users
    - Security: HTTPS, data encryption, secure payment processing
    """
    
    print("🧪 Testing Improved RequirementAnalyzer...")
    print("=" * 60)
    
    try:
        # Initialize the analyzer
        analyzer = RequirementAnalyzer()
        print("✓ RequirementAnalyzer initialized with improved prompts")
        
        # Analyze the sample requirements
        print("🔍 Analyzing requirements with improved categorization...")
        print("⚠️  Note: This will create distinct frontend and backend documents...")
        results = await analyzer.analyze_requirements(sample_text)
        
        # Save the results
        print("💾 Saving differentiated SRDs...")
        frontend_path, backend_path = await analyzer.save_srds(results, "test_output")
        
        print("✅ Analysis completed successfully!")
        print(f"📄 Frontend SRD saved to: {frontend_path}")
        print(f"📄 Backend SRD saved to: {backend_path}")
        
        # Show previews of both documents to demonstrate differentiation
        print("\n" + "=" * 60)
        print("📊 FRONTEND SRD PREVIEW:")
        print("=" * 60)
        frontend_preview = results["frontend_srd"][:800] + "..." if len(results["frontend_srd"]) > 800 else results["frontend_srd"]
        print(frontend_preview)
        
        print("\n" + "=" * 60)
        print("📊 BACKEND SRD PREVIEW:")
        print("=" * 60)
        backend_preview = results["backend_srd"][:800] + "..." if len(results["backend_srd"]) > 800 else results["backend_srd"]
        print(backend_preview)
        
        print("\n" + "=" * 60)
        print("📊 ANALYSIS PREVIEW:")
        print("=" * 60)
        analysis_preview = results["analysis"][:600] + "..." if len(results["analysis"]) > 600 else results["analysis"]
        print(analysis_preview)
        
        # Check for differentiation
        print("\n" + "=" * 60)
        print("🔍 DIFFERENTIATION CHECK:")
        print("=" * 60)
        
        frontend_words = set(results["frontend_srd"].lower().split())
        backend_words = set(results["backend_srd"].lower().split())
        
        # Check for frontend-specific terms
        frontend_terms = ['ui', 'interface', 'component', 'react', 'client', 'browser', 'responsive']
        backend_terms = ['database', 'api', 'server', 'authentication', 'postgresql', 'endpoint']
        
        frontend_score = sum(1 for term in frontend_terms if term in frontend_words)
        backend_score = sum(1 for term in backend_terms if term in backend_words)
        
        print(f"Frontend-specific terms found: {frontend_score}/{len(frontend_terms)}")
        print(f"Backend-specific terms found: {backend_score}/{len(backend_terms)}")
        
        if frontend_score >= 3 and backend_score >= 3:
            print("✅ Documents appear to be properly differentiated!")
        else:
            print("⚠️  Documents may not be sufficiently differentiated.")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set the OPENAI_API_KEY environment variable")
        print("2. Installed all required dependencies with latest versions")
        print("3. Run: python fix_dependencies.py")

async def main():
    """Main test function"""
    print("🚀 Improved Requirements Analyzer Test Suite")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key")
        return
    
    # Create test output directory
    Path("test_output").mkdir(exist_ok=True)
    
    # Test improved requirement analyzer
    await test_improved_analyzer()

if __name__ == "__main__":
    asyncio.run(main())