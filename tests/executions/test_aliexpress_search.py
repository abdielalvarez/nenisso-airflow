"""
Test execution for AliExpress item_search_5
Run with: python tests/executions/test_aliexpress_search.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_search():
    """Simple test of AliExpress item search"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    try:
        result = api.item_search_5(q="iphone", page=1)
        print("✅ AliExpress API working")
        print(f"Items found: {len(result.get('result', {}).get('resultList', []))}")
        
        # Print complete payload
        import json
        print("\n📦 Complete API Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_search()