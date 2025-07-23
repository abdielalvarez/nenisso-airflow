"""
Test execution for AliExpress item_sku
Run with: python tests/executions/test_aliexpress_sku.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_sku():
    """Test AliExpress item SKU/variants endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known working item ID
    item_id = "3256809212376891"
    
    try:
        print(f"🔍 Testing item_sku with itemId: {item_id}")
        result = api.item_sku(
            item_id=item_id,
            currency="MXN",
            region="MX",
            locale="es_ES"
        )
        
        sku_info = result.get('result', {}).get('skuInfo', {})
        sku_props = sku_info.get('skuProps', [])
        print(f"✅ SKU options retrieved: {len(sku_props)}")
        
        if sku_props:
            first_sku = sku_props[0]
            print(f"First SKU property: {first_sku.get('propName', 'N/A')}")
        
        # Print complete payload
        import json
        print("\n📦 Complete SKU Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_sku()