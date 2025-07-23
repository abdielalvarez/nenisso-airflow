"""
Test execution for AliExpress item_review_2
Run with: python tests/executions/test_aliexpress_reviews.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.aliexpress import AliExpress
from include.configs.env_config import ENV

def test_aliexpress_reviews():
    """Test AliExpress item reviews endpoint"""
    api_key = ENV.get('RAPIDAPI_ALIEXPRESS_KEY')
    
    if not api_key:
        print("❌ RAPIDAPI_ALIEXPRESS_KEY not found in .env")
        return
    
    api = AliExpress(api_key)
    
    # Use known working item ID
    item_id = "3256809212376891"
    
    try:
        print(f"🔍 Testing item_review_2 with itemId: {item_id}")
        result = api.item_review_2(
            item_id=item_id,
            page=1,
            filter_type="allReviews",
            region="MX",
            locale="es_ES"
        )
        
        reviews = result.get('result', {}).get('reviews', [])
        print(f"✅ Reviews retrieved: {len(reviews)}")
        
        if reviews:
            first_review = reviews[0]
            print(f"First review rating: {first_review.get('rating', 'N/A')}")
            print(f"Review text: {first_review.get('content', 'N/A')[:100]}...")
        
        # Print complete payload
        import json
        print("\n📦 Complete Reviews Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aliexpress_reviews()