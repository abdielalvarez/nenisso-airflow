"""
Test execution for AliExpress shipping_detail_5
Run with: python tests/executions/test_aliexpress_shipping.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_shipping():
    """Test AliExpress shipping details endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known working item ID
    item_id = "3256809212376891"
    
    try:
        print(f"🔍 Testing shipping_detail_5 with itemId: {item_id}")
        result = api.shipping_detail_5(
            item_id=item_id,
            quantity=1,
            region="MX",
            locale="es_ES",
            currency="MXN"
        )
        
        shipping_info = result.get('result', {}).get('shippingInfo', [])
        print(f"✅ Shipping options retrieved: {len(shipping_info)}")
        
        if shipping_info:
            first_option = shipping_info[0]
            print(f"First shipping option: {first_option.get('serviceName', 'N/A')}")
        
        # Print complete payload
        import json
        print("\n📦 Complete Shipping Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_shipping()