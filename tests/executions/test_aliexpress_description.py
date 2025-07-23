"""
Test execution for AliExpress item_desc_2
Run with: python tests/executions/test_aliexpress_description.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_description():
    """Test AliExpress item description endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known working item ID
    item_id = "3256809212376891"
    
    try:
        print(f"🔍 Testing item_desc_2 with itemId: {item_id}")
        result = api.item_desc_2(item_id, locale="es_ES")
        
        description = result.get('result', {}).get('description', '')
        print(f"✅ Description retrieved: {len(description)} characters")
        print(f"Description preview: {description[:200]}...")
        
        # Print complete payload
        import json
        print("\n📦 Complete Description Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_description()