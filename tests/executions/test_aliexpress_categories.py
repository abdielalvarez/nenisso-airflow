"""
Test execution for AliExpress category_list_1
Run with: python tests/executions/test_aliexpress_categories.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_categories():
    """Test AliExpress categories list endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    try:
        print("🔍 Testing category_list_1")
        result = api.category_list_1(locale="es_ES")
        
        categories = result.get('result', {}).get('categories', [])
        print(f"✅ Categories retrieved: {len(categories)}")
        
        if categories:
            print(f"First category: {categories[0].get('name', 'N/A')}")
        
        # Print complete payload
        import json
        print("\n📦 Complete Categories Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_categories()