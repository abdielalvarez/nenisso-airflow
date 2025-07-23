"""
Test execution for AliExpress store_info
Run with: python tests/executions/test_aliexpress_store_info.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_store_info():
    """Test AliExpress store information endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known seller ID from n8n workflows
    seller_id = "231651707"
    
    try:
        print(f"🔍 Testing store_info for seller: {seller_id}")
        result = api.store_info(
            seller_id=seller_id,
            currency="MXN",
            region="MX",
            locale="es_ES"
        )
        
        store_title = result.get('result', {}).get('storeTitle', 'N/A')
        store_rating = result.get('result', {}).get('storeRating', 'N/A')
        print(f"✅ Store info retrieved: {store_title}")
        print(f"Store rating: {store_rating}")
        
        # Print complete payload
        import json
        print("\n📦 Complete Store Info Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_store_info()