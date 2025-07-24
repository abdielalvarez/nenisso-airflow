"""
PostgreSQL Service Integration
Migrated from n8n PostgreSQL nodes to provide centralized database operations
Original n8n credential ID: K41z3jc09qjD5iD5 ("Postgres account")
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Postgres:
    """
    PostgreSQL service class for nenisso-airflow project
    Provides methods for error_handling table and aliexpress_search_garbage_scoring table
    Migrated from n8n workflows with schema: nenisso-ecommerce
    """
    
    def __init__(self, connection_string: str, default_schema: str = "nenisso-ecommerce"):
        """
        Initialize PostgreSQL connection
        
        Args:
            connection_string: PostgreSQL connection string
            default_schema: Default schema name (from n8n workflows)
        """
        self.connection_string = connection_string
        self.default_schema = default_schema
        
        # Test connection on initialization
        try:
            self._test_connection()
            logger.info("PostgreSQL connection established successfully")
        except Exception as e:
            logger.error(f"Failed to establish PostgreSQL connection: {e}")
            raise
    
    def _test_connection(self):
        """Test database connection"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result is None or result[0] != 1:
                    raise ConnectionError("Database connection test failed")
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            conn.autocommit = False
            
            # Set search path to include nenisso-ecommerce schema
            with conn.cursor() as cursor:
                cursor.execute('SET search_path TO "nenisso-ecommerce", public;')
            
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    # ERROR_HANDLING TABLE OPERATIONS
    # Migrated from n8n error_handling table operations
    
    def insert_error_handling(self, 
                             api_source: str, 
                             workflow_name: str, 
                             status_code: Optional[int] = None,
                             error_message: Optional[Union[Dict, str]] = None,
                             api_request: Optional[Union[Dict, str]] = None,
                             violation_details: Optional[str] = None) -> Dict[str, Any]:
        """
        Insert record into error_handling table
        Migrated from n8n PostgreSQL insert operations
        Original table: nenisso-ecommerce.error_handling
        
        Args:
            api_source: Source API identifier (e.g., "reviews_for_listing")
            workflow_name: n8n workflow name (e.g., "MERCADO LIBRE LISTINGS FOR SEARCH")
            status_code: HTTP status code
            error_message: Error details (will be stored as JSONB)
            api_request: Original request data (will be stored as JSONB)
            violation_details: Additional error context
            
        Returns:
            Dict with insertion status and record ID
        """
        try:
            # Convert objects to JSON if needed (matches n8n node behavior)
            error_message_json = json.dumps(error_message) if isinstance(error_message, dict) else error_message
            api_request_json = json.dumps(api_request) if isinstance(api_request, dict) else api_request
            
            insert_query = sql.SQL("""
                INSERT INTO error_handling 
                (api_source, workflow_name, status_code, error_message, api_request, violation_details, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """)
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, (
                        api_source,
                        workflow_name,
                        status_code,
                        error_message_json,
                        api_request_json,
                        violation_details,
                        datetime.now()
                    ))
                    
                    # Get the inserted record ID
                    result = cursor.fetchone()
                    if result is None:
                        raise RuntimeError("INSERT operation failed to return record ID")
                    record_id = result[0]
                    conn.commit()
                    
            logger.info(f"Record inserted into error_handling table (ID: {record_id})")
            
            return {
                'status': 'inserted',
                'id': record_id,
                'api_source': api_source,
                'workflow_name': workflow_name,
                'status_code': status_code,
                'inserted': True
            }
            
        except Exception as e:
            logger.error(f"Failed to insert into error_handling table: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'api_source': api_source,
                'workflow_name': workflow_name,
                'inserted': False
            }
    
    # ALIEXPRESS_SEARCH_GARBAGE_SCORING TABLE OPERATIONS
    # Migrated from n8n workflow: PARENT_-_GENERATE_JSON_AND_UPLOAD_TO_STORAGE_sEMD8hABKqlrvAK4.json
    
    def insert_aliexpress_garbage_scoring(self, 
                                        search_id: str,
                                        total_items: int,
                                        valid_items: int, 
                                        invalid_items: int,
                                        garbage_percentage: float) -> Dict[str, Any]:
        """
        Insert AliExpress search garbage scoring data
        Migrated from n8n workflow: PARENT_-_GENERATE_JSON_AND_UPLOAD_TO_STORAGE_sEMD8hABKqlrvAK4.json
        Original table: nenisso-ecommerce.aliexpress_search_garbage_scoring
        
        Args:
            search_id: Foreign key reference to search term (from PARSING node term_id)
            total_items: Total items in search results
            valid_items: Count of relevant items (determined by AI analysis)
            invalid_items: Count of irrelevant items (determined by AI analysis)
            garbage_percentage: Decimal from 0.0 to 1.0 (invalid_items / total_items)
            
        Returns:
            Dict with insertion status and quality assessment
        """
        try:
            # Quality control logic from n8n workflow
            quality_threshold = 0.5  # 50% garbage threshold from original workflow
            is_high_quality = garbage_percentage < quality_threshold
            
            # Validate input data
            if total_items != (valid_items + invalid_items):
                logger.warning(f"Item count mismatch: total={total_items}, valid+invalid={valid_items + invalid_items}")
            
            if not (0.0 <= garbage_percentage <= 1.0):
                raise ValueError(f"garbage_percentage must be between 0.0 and 1.0, got {garbage_percentage}")
            
            insert_query = sql.SQL("""
                INSERT INTO aliexpress_search_garbage_scoring 
                (search_id, total_items, valid_items, invalid_items, garbage_percentage)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """)
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, (
                        search_id,
                        total_items,
                        valid_items,
                        invalid_items,
                        garbage_percentage
                    ))
                    
                    # Get the inserted record ID
                    result = cursor.fetchone()
                    if result is None:
                        raise RuntimeError("INSERT operation failed to return record ID")
                    scoring_id = result[0]
                    conn.commit()
            
            logger.info(f"Garbage scoring inserted for search_id {search_id}: {garbage_percentage:.2%} garbage (ID: {scoring_id})")
            
            return {
                'status': 'inserted',
                'id': scoring_id,
                'search_id': search_id,
                'total_items': total_items,
                'valid_items': valid_items,
                'invalid_items': invalid_items,
                'garbage_percentage': garbage_percentage,
                'quality_assessment': 'high_quality' if is_high_quality else 'high_garbage',
                'should_continue_processing': is_high_quality,
                'threshold_used': quality_threshold,
                'inserted': True
            }
            
        except Exception as e:
            logger.error(f"Failed to insert garbage scoring for search_id {search_id}: {e}")
            
            return {
                'status': 'error',
                'error': str(e),
                'search_id': search_id,
                'inserted': False
            }