"""
Test execution for AliExpress store_item_search_2
Run with: python tests/executions/test_aliexpress_store_search.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_store_search():
    """Test AliExpress store item search endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known store IDs from n8n workflows
    store_id = "1102051418"
    seller_id = "231651707"
    
    try:
        print(f"🔍 Testing store_item_search_2 for store: {store_id}")
        result = api.store_item_search_2(
            store_id=store_id,
            seller_id=seller_id,
            page=1,
            page_size=5
        )
        
        items = result.get('result', {}).get('resultList', [])
        print(f"✅ Store items retrieved: {len(items)}")
        
        if items:
            first_item = items[0].get('item', {})
            print(f"First item: {first_item.get('title', 'N/A')[:50]}...")
        
        # Print complete payload
        import json
        print("\n📦 Complete Store Search Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_store_search()