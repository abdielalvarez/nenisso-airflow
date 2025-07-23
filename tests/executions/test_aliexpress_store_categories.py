"""
Test execution for AliExpress store_categories
Run with: python tests/executions/test_aliexpress_store_categories.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_store_categories():
    """Test AliExpress store categories endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known store IDs from n8n workflows
    store_id = "1102051418"
    seller_id = "231651707"
    
    try:
        print(f"🔍 Testing store_categories for store: {store_id}")
        result = api.store_categories(
            seller_id=seller_id,
            store_id=store_id,
            currency="MXN",
            region="MX"
        )
        
        categories = result.get('result', {}).get('categories', [])
        print(f"✅ Store categories retrieved: {len(categories)}")
        
        if categories:
            first_category = categories[0]
            print(f"First category: {first_category.get('name', 'N/A')}")
        
        # Print complete payload
        import json
        print("\n📦 Complete Store Categories Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_store_categories()