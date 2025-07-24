"""
Test execution for PostgreSQL aliexpress_search_garbage_scoring table insertion
Run with: python tests/executions/test_postgres_garbage_scoring.py
"""
import sys
import os
import time
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.postgres import Postgres
from include.configs.env_config import ENV

def test_postgres_garbage_scoring():
    """Test inserting into aliexpress_search_garbage_scoring table"""
    
    # Get PostgreSQL connection string from environment
    connection_string = ENV.get('POSTGRES_CONNECTION_STRING')
    
    if not connection_string:
        print("❌ POSTGRES_CONNECTION_STRING not found in .env")
        print("Add to your .env file:")
        print("POSTGRES_CONNECTION_STRING=postgresql://user:password@host:port/database")
        return
    
    try:
        # Initialize PostgreSQL service
        pg = Postgres(connection_string)
        print("✅ PostgreSQL connection established")
        
        # Test case 1: High quality search (low garbage percentage)
        print("\n📝 Test Case 1: High quality search results (30% garbage)...")
        high_quality_data: Dict[str, Any] = {
            'search_id': f'search_high_quality_{int(time.time())}',
            'total_items': 20,
            'valid_items': 14,
            'invalid_items': 6,
            'garbage_percentage': 0.3  # 30% garbage (below 50% threshold)
        }
        
        result1 = pg.insert_aliexpress_garbage_scoring(**high_quality_data)
        
        if result1.get('inserted'):
            print("✅ High quality scoring record inserted successfully")
            print(f"   Record ID: {result1['id']}")
            print(f"   Search ID: {result1['search_id']}")
            print(f"   Total Items: {result1['total_items']}")
            print(f"   Valid Items: {result1['valid_items']}")
            print(f"   Invalid Items: {result1['invalid_items']}")
            print(f"   Garbage Percentage: {result1['garbage_percentage']:.1%}")
            print(f"   Quality Assessment: {result1['quality_assessment']}")
            print(f"   Should Continue Processing: {result1['should_continue_processing']}")
        else:
            print("❌ Failed to insert high quality scoring record")
            print(f"   Error: {result1.get('error')}")
        
        # Test case 2: Low quality search (high garbage percentage)
        print("\n📝 Test Case 2: Low quality search results (70% garbage)...")
        low_quality_data: Dict[str, Any] = {
            'search_id': f'search_low_quality_{int(time.time())}',
            'total_items': 25,
            'valid_items': 7,
            'invalid_items': 18,
            'garbage_percentage': 0.72  # 72% garbage (above 50% threshold)
        }
        
        result2 = pg.insert_aliexpress_garbage_scoring(**low_quality_data)
        
        if result2.get('inserted'):
            print("✅ Low quality scoring record inserted successfully")
            print(f"   Record ID: {result2['id']}")
            print(f"   Search ID: {result2['search_id']}")
            print(f"   Total Items: {result2['total_items']}")
            print(f"   Valid Items: {result2['valid_items']}")
            print(f"   Invalid Items: {result2['invalid_items']}")
            print(f"   Garbage Percentage: {result2['garbage_percentage']:.1%}")
            print(f"   Quality Assessment: {result2['quality_assessment']}")
            print(f"   Should Continue Processing: {result2['should_continue_processing']}")
        else:
            print("❌ Failed to insert low quality scoring record")
            print(f"   Error: {result2.get('error')}")
        
        # Test case 3: Edge case - exactly at threshold (50% garbage)
        print("\n📝 Test Case 3: Threshold edge case (50% garbage)...")
        threshold_data: Dict[str, Any] = {
            'search_id': f'search_threshold_{int(time.time())}',
            'total_items': 10,
            'valid_items': 5,
            'invalid_items': 5,
            'garbage_percentage': 0.5  # Exactly 50% garbage (at threshold)
        }
        
        result3 = pg.insert_aliexpress_garbage_scoring(**threshold_data)
        
        if result3.get('inserted'):
            print("✅ Threshold scoring record inserted successfully")
            print(f"   Record ID: {result3['id']}")
            print(f"   Search ID: {result3['search_id']}")
            print(f"   Garbage Percentage: {result3['garbage_percentage']:.1%}")
            print(f"   Quality Assessment: {result3['quality_assessment']}")
            print(f"   Should Continue Processing: {result3['should_continue_processing']}")
            print(f"   Threshold Used: {result3['threshold_used']}")
        else:
            print("❌ Failed to insert threshold scoring record")
            print(f"   Error: {result3.get('error')}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")


def test_garbage_scoring_validation():
    """Test validation logic for garbage scoring"""
    
    connection_string = ENV.get('POSTGRES_CONNECTION_STRING')
    
    if not connection_string:
        print("❌ POSTGRES_CONNECTION_STRING not found in .env")
        return
    
    try:
        pg = Postgres(connection_string)
        print("✅ PostgreSQL connection established")
        
        # Test invalid garbage percentage (> 1.0)
        print("\n📝 Testing validation: Invalid garbage percentage (> 1.0)...")
        invalid_data: Dict[str, Any] = {
            'search_id': f'search_invalid_{int(time.time())}',
            'total_items': 10,
            'valid_items': 8,
            'invalid_items': 2,
            'garbage_percentage': 1.5  # Invalid: > 1.0
        }
        
        result = pg.insert_aliexpress_garbage_scoring(**invalid_data)
        
        if not result.get('inserted'):
            print("✅ Validation correctly rejected invalid garbage percentage")
            print(f"   Error: {result.get('error')}")
        else:
            print("❌ Validation failed - should have rejected invalid percentage")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")


if __name__ == "__main__":
    print("🧪 Testing PostgreSQL AliExpress Garbage Scoring Table")
    print("=" * 60)
    
    print("\n1. Testing garbage scoring insertions:")
    test_postgres_garbage_scoring()
    
    print("\n2. Testing validation logic:")
    test_garbage_scoring_validation()
    
    print("\n✅ Garbage scoring tests completed!")