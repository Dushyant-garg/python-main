#!/usr/bin/env python3
"""
Test script for the feedback workflow with user proxy agent
"""

import asyncio
import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

async def test_feedback_workflow():
    """Test the complete feedback workflow"""
    print("🧪 Testing Feedback Workflow")
    print("=" * 50)
    
    # Test data - simulated feedback scenarios
    test_scenarios = [
        {
            "srd_type": "frontend",
            "feedback": "Please add more details about user authentication flow and responsive design requirements.",
            "original_analysis": "Sample e-commerce project requiring user management and shopping features."
        },
        {
            "srd_type": "backend", 
            "feedback": "Include specific database requirements and API rate limiting specifications.",
            "original_analysis": "Sample e-commerce project requiring user management and shopping features."
        }
    ]
    
    print("📋 Testing feedback scenarios...")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 Test {i}: {scenario['srd_type'].title()} SRD Feedback")
        
        try:
            # Test the regenerate API endpoint
            payload = {
                "srd_type": scenario["srd_type"],
                "feedback": scenario["feedback"],
                "original_analysis": scenario["original_analysis"]
            }
            
            print(f"📤 Sending feedback: {scenario['feedback'][:50]}...")
            
            response = requests.post(f"{API_BASE_URL}/regenerate-srd", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result['message']}")
                
                # Check if content was generated
                content_key = f"{scenario['srd_type']}_srd"
                if result.get(content_key):
                    content_length = len(result[content_key])
                    print(f"📄 Generated {scenario['srd_type']} SRD: {content_length} characters")
                    
                    # Show a preview
                    preview = result[content_key][:200].replace('\n', ' ')
                    print(f"📝 Preview: {preview}...")
                else:
                    print(f"⚠️  No {scenario['srd_type']} content in response")
                    
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the FastAPI server is running on localhost:8000")
            print("💡 Run: python run_ui.py")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False
    
    print("\n🎯 Testing UI Integration...")
    
    # Test the health endpoint
    try:
        health_response = requests.get(f"{API_BASE_URL}/")
        if health_response.status_code == 200:
            print("✅ API server is responsive")
        else:
            print(f"⚠️  API server responded with: {health_response.status_code}")
    except Exception as e:
        print(f"❌ API health check failed: {str(e)}")
        return False
    
    print("\n🎉 Feedback workflow test completed!")
    print("\n📋 Next Steps:")
    print("1. Start the application: python run_ui.py")
    print("2. Upload a document")
    print("3. Click 'Reject' on any SRD")
    print("4. Provide feedback and click 'Regenerate'")
    print("5. Verify the SRD is updated with your feedback")
    
    return True

def test_ui_components():
    """Test UI component existence"""
    print("\n🖥️  Testing UI Components...")
    
    ui_file = Path("streamlit_ui.py")
    if not ui_file.exists():
        print("❌ streamlit_ui.py not found")
        return False
    
    ui_content = ui_file.read_text()
    
    # Check for key components
    required_components = [
        "regenerate_srd",
        "show_frontend_feedback", 
        "show_backend_feedback",
        "text_area",
        "Regenerate Frontend",
        "Regenerate Backend"
    ]
    
    for component in required_components:
        if component in ui_content:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            return False
    
    print("✅ All UI components found")
    return True

if __name__ == "__main__":
    print("🚀 Starting Feedback Workflow Tests")
    
    # Test UI components first
    ui_test_passed = test_ui_components()
    
    if ui_test_passed:
        print("\n" + "="*50)
        # Test the actual workflow
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            workflow_test_passed = loop.run_until_complete(test_feedback_workflow())
        finally:
            loop.close()
    else:
        print("❌ UI component tests failed")
        workflow_test_passed = False
    
    if ui_test_passed and workflow_test_passed:
        print("\n🎉 All tests passed! The feedback workflow is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")