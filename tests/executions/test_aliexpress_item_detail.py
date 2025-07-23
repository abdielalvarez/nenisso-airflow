"""
Test execution for AliExpress item_detail_3
Run with: python tests/executions/test_aliexpress_item_detail.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_item_detail():
    """Test AliExpress item detail endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use the known working item ID from the mock
    item_id = "3256809212376891"
    
    try:
        print(f"🔍 Testing item_detail_3 with itemId: {item_id}")
        detail_result = api.item_detail_3(item_id)
        
        item_detail = detail_result.get('result', {}).get('item', {})
        print(f"✅ Item detail retrieved")
        print(f"Title: {item_detail.get('title', 'N/A')[:100]}")
        print(f"Available: {item_detail.get('available', 'N/A')}")
        print(f"Price: {item_detail.get('sku', {}).get('def', {}).get('price', 'N/A')}")
        
        # Print complete payload
        import json
        print("\n📦 Complete Item Detail Response:")
        print(json.dumps(detail_result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_item_detail()