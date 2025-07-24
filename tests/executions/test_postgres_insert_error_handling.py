"""
Test execution for PostgreSQL error_handling table insertion
Run with: python tests/executions/test_postgres_error_handling.py
"""
import sys
import os
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from services.postgres import Postgres
from include.configs.env_config import ENV

def test_postgres_error_handling():
    """Test inserting into error_handling table"""
    
    # Initialize PostgreSQL service using env config
    connection_string = f"postgresql://{ENV['DB_POSTGRESDB_USER']}:{ENV['DB_POSTGRESDB_PASSWORD']}@{ENV['DB_POSTGRESDB_HOST']}:{ENV['DB_POSTGRESDB_PORT']}/{ENV['DB_POSTGRESDB_DATABASE']}"
    
    try:
        pg = Postgres(connection_string)
        print("✅ PostgreSQL connection established")
        
        # Test data for error_handling table
        test_error_data: Dict[str, Any] = {
            'api_source': 'reviews_for_listing',
            'workflow_name': 'MERCADO LIBRE LISTINGS FOR SEARCH',
            'status_code': 500,  # int value
            'error_message': {
                'error_type': 'API_ERROR',
                'message': 'Internal server error from MercadoLibre API',
                'details': 'Connection timeout while fetching product reviews',
                'timestamp': '2025-01-24T10:30:00Z'
            },
            'api_request': {
                'method': 'GET',
                'url': 'https://api.mercadolibre.com/reviews/listing/123456',
                'headers': {'Authorization': 'Bearer token_hidden'},
                'params': {'limit': 50, 'offset': 0}
            },
            'violation_details': 'HTTP 500 - Internal Server Error'
        }
        
        # Insert into error_handling table
        print("📝 Inserting error handling record...")
        result = pg.insert_error_handling(**test_error_data)
        
        if result.get('inserted'):
            print("✅ Error handling record inserted successfully")
            print(f"   Record ID: {result['id']}")
            print(f"   API Source: {result['api_source']}")
            print(f"   Workflow Name: {result['workflow_name']}")
            print(f"   Status Code: {result['status_code']}")
            print(f"   Status: {result['status']}")
        else:
            print("❌ Failed to insert error handling record")
            print(f"   Error: {result.get('error')}")
            
        # Test with minimal data (None values for optional fields)
        print("\n📝 Testing with minimal data (None values)...")
        minimal_data: Dict[str, Any] = {
            'api_source': 'test_minimal_api',
            'workflow_name': 'TEST_MINIMAL_WORKFLOW',
            'status_code': None,  # Explicitly set to None
            'error_message': None,  # Explicitly set to None
            'api_request': None,  # Explicitly set to None
            'violation_details': None  # Explicitly set to None
        }
        
        result_minimal = pg.insert_error_handling(**minimal_data)
        
        if result_minimal.get('inserted'):
            print("✅ Minimal error record inserted successfully")
            print(f"   Record ID: {result_minimal['id']}")
        else:
            print("❌ Failed to insert minimal error record")
            print(f"   Error: {result_minimal.get('error')}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")


if __name__ == "__main__":
    print("🧪 Testing PostgreSQL Error Handling Table")
    print("=" * 50)
    test_postgres_error_handling()
    print("\n✅ Error handling test completed!")