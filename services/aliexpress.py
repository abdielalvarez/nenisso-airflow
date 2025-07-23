"""
AliExpress API integration using RapidAPI
Based on n8n implementation with endpoints like item_search_5
"""
import requests
import logging
from typing import Dict, Any, Optional


class AliExpress:
    """
    AliExpress API integration class using RapidAPI
    Handles all AliExpress DataHub API endpoints with proper error handling
    """
    
    def __init__(self, rapidapi_key: str):
        """
        Initialize AliExpress API client
        
        Args:
            rapidapi_key: RapidAPI key for authentication
        """
        self.rapidapi_key = rapidapi_key
        self.base_url = "https://aliexpress-datahub.p.rapidapi.com"
        self.headers = {
            'x-rapidapi-host': 'aliexpress-datahub.p.rapidapi.com',
            'x-rapidapi-key': rapidapi_key
        }
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make HTTP request to AliExpress API with proper error handling
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if not self._validate_response(data):
                raise ValueError(f"Invalid response from {endpoint}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {endpoint}: {str(e)}")
            raise
        except ValueError as e:
            self.logger.error(f"Response validation failed for {endpoint}: {str(e)}")
            raise
    
    def _validate_response(self, data: Dict[str, Any]) -> bool:
        """
        Validate API response structure following n8n patterns
        """
        if not isinstance(data, dict):
            return False
        
        result = data.get('result', {})
        status = result.get('status', {})
        
        # Valid response codes: 200 (success), 205 (no results)
        valid_codes = [200, 205]
        code = status.get('code')
        
        if code not in valid_codes:
            self.logger.error(f"API returned invalid code: {status}")
            return False
        
        if status.get('violations'):
            self.logger.error(f"API violations: {status.get('violations')}")
            return False
        
        # Code 205 with data="error" is valid (no results found)
        if code == 205 and status.get('data') == 'error':
            self.logger.info(f"No results found: {status.get('msg')}")
            return True
        
        # Code 200 should not have data="error"
        if code == 200 and status.get('data') == 'error':
            self.logger.error(f"API data error: {status.get('msg')}")
            return False
        
        return True
    
    def item_search_5(self, 
                      q: str, 
                      page: int = 1,
                      sort: str = "default",
                      loc: str = "MX",
                      start_price: Optional[str] = None,
                      end_price: Optional[str] = None,
                      locale: str = "es_ES",
                      region: str = "MX",
                      currency: str = "MXN") -> Dict[str, Any]:
        """
        Search AliExpress items by keyword
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/item_search_5?q=iphone&page=1&sort=default'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            q: Search keyword (e.g., "iphone")
            page: Page number (default: 1)
            sort: Sort order (default, price_low_to_high, price_high_to_low, etc.)
            loc: Location code (default: "MX")
            start_price: Minimum price filter
            end_price: Maximum price filter
            locale: Language locale (default: "es_ES")
            region: Region code (default: "MX")
            currency: Currency code (default: "MXN")
            
        Returns:
            API response with search results
        """
        params = {
            'q': q,
            'page': str(page),
            'sort': sort,
            'loc': loc,
            'locale': locale,
            'region': region,
            'currency': currency
        }
        
        # Add optional price filters
        if start_price:
            params['startPrice'] = start_price
        if end_price:
            params['endPrice'] = end_price
        
        self.logger.info(f"Searching AliExpress for: {q}, page: {page}")
        
        try:
            response = self._make_request('item_search_5', params)
            items_count = len(response.get('result', {}).get('resultList', []))
            self.logger.info(f"Found {items_count} items for query: {q}")
            return response
            
        except Exception as e:
            self.logger.error(f"item_search_5 failed for query '{q}': {str(e)}")
            raise
    
    def item_detail_3(self, 
                      item_id: str,
                      currency: str = "MXN",
                      region: str = "MX", 
                      locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get detailed information for a specific AliExpress item
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/item_detail_3?itemId=1005009259306474&currency=MXN&region=MX&locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            item_id: AliExpress item ID (e.g., "1005009259306474")
            currency: Currency code (default: "MXN")
            region: Region code (default: "MX")
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with detailed item information
        """
        params = {
            'itemId': str(item_id),
            'currency': currency,
            'region': region,
            'locale': locale
        }
        
        self.logger.info(f"Getting item details for: {item_id}")
        
        try:
            response = self._make_request('item_detail_3', params)
            
            # Additional validations from n8n workflow
            item = response.get('result', {}).get('item', {})
            
            # Validate itemId matches
            response_item_id = str(item.get('itemId', ''))
            if response_item_id != str(item_id):
                self.logger.warning(f"ItemId mismatch: requested {item_id}, got {response_item_id}")
            
            # Check if item is available
            if not item.get('available', False):
                self.logger.warning(f"Item {item_id} is not available")
            
            # Check SKU availability
            sku_quantity = item.get('sku', {}).get('def', {}).get('quantity', 0)
            if sku_quantity <= 0:
                self.logger.warning(f"Item {item_id} has no stock (quantity: {sku_quantity})")
            
            self.logger.info(f"Item details retrieved for: {item.get('title', 'N/A')[:50]}...")
            return response
            
        except Exception as e:
            self.logger.error(f"item_detail_3 failed for item_id '{item_id}': {str(e)}")
            raise
    
    def category_list_1(self, locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get AliExpress categories list
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/category_list_1?locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with categories list
        """
        params = {
            'locale': locale
        }
        
        self.logger.info(f"Getting AliExpress categories for locale: {locale}")
        
        try:
            response = self._make_request('category_list_1', params)
            categories_count = len(response.get('result', {}).get('categories', []))
            self.logger.info(f"Retrieved {categories_count} categories")
            return response
            
        except Exception as e:
            self.logger.error(f"category_list_1 failed for locale '{locale}': {str(e)}")
            raise
    
    def item_desc_2(self, item_id: str, locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get detailed description for a specific AliExpress item
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/item_desc_2?itemId=1005005244562338&locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            item_id: AliExpress item ID (e.g., "1005005244562338")
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with detailed item description
        """
        params = {
            'itemId': str(item_id),
            'locale': locale
        }
        
        self.logger.info(f"Getting item description for: {item_id}")
        
        try:
            response = self._make_request('item_desc_2', params)
            description_length = len(response.get('result', {}).get('description', ''))
            self.logger.info(f"Retrieved description with {description_length} characters")
            return response
            
        except Exception as e:
            self.logger.error(f"item_desc_2 failed for item_id '{item_id}': {str(e)}")
            raise
    
    def store_item_search_2(self, 
                            store_id: str, 
                            seller_id: str,
                            page: int = 1,
                            page_size: int = 20,
                            sort: str = "default",
                            locale: str = "es_ES",
                            currency: str = "MXN",
                            region: str = "MX") -> Dict[str, Any]:
        """
        Search items within a specific AliExpress store
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/store_item_search_2?storeId=1102051418&sellerId=231651707&sort=default&page=1&pageSize=20&locale=es_ES&currency=MXN&region=MX'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            store_id: Store ID (e.g., "1102051418")
            seller_id: Seller ID (e.g., "231651707")
            page: Page number (default: 1)
            page_size: Items per page (default: 20)
            sort: Sort order (default: "default")
            locale: Language locale (default: "es_ES")
            currency: Currency code (default: "MXN")
            region: Region code (default: "MX")
            
        Returns:
            API response with store items
        """
        params = {
            'storeId': str(store_id),
            'sellerId': str(seller_id),
            'sort': sort,
            'page': str(page),
            'pageSize': str(page_size),
            'locale': locale,
            'currency': currency,
            'region': region
        }
        
        self.logger.info(f"Searching store {store_id} items, page: {page}")
        
        try:
            response = self._make_request('store_item_search_2', params)
            items_count = len(response.get('result', {}).get('resultList', []))
            self.logger.info(f"Found {items_count} items in store {store_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"store_item_search_2 failed for store '{store_id}': {str(e)}")
            raise
    
    def shipping_detail_5(self, 
                          item_id: str,
                          quantity: int = 1,
                          region: str = "MX",
                          locale: str = "es_ES",
                          currency: str = "MXN",
                          ext: Optional[str] = None) -> Dict[str, Any]:
        """
        Get shipping details for a specific AliExpress item
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/shipping_detail_5?itemId=1005005244562338&quantity=1&region=MX&locale=es_ES&currency=MXN'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            item_id: AliExpress item ID (e.g., "1005005244562338")
            quantity: Quantity (default: 1)
            region: Region code (default: "MX")
            locale: Language locale (default: "es_ES")
            currency: Currency code (default: "MXN")
            ext: Extended parameter (optional)
            
        Returns:
            API response with shipping details
        """
        params = {
            'itemId': str(item_id),
            'quantity': str(quantity),
            'region': region,
            'locale': locale,
            'currency': currency
        }
        
        if ext:
            params['ext'] = ext
        
        self.logger.info(f"Getting shipping details for item: {item_id}")
        
        try:
            response = self._make_request('shipping_detail_5', params)
            shipping_options = len(response.get('result', {}).get('shippingInfo', []))
            self.logger.info(f"Retrieved {shipping_options} shipping options")
            return response
            
        except Exception as e:
            self.logger.error(f"shipping_detail_5 failed for item_id '{item_id}': {str(e)}")
            raise
    
    def item_review_2(self, 
                      item_id: str,
                      page: int = 1,
                      filter_type: str = "allReviews",
                      region: str = "MX",
                      locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get reviews for a specific AliExpress item
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/item_review_2?itemId=1005005244562338&page=1&filter=allReviews&region=MX&locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            item_id: AliExpress item ID (e.g., "1005005244562338")
            page: Page number (default: 1)
            filter_type: Review filter (default: "allReviews")
            region: Region code (default: "MX")
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with item reviews
        """
        params = {
            'itemId': str(item_id),
            'page': str(page),
            'filter': filter_type,
            'region': region,
            'locale': locale
        }
        
        self.logger.info(f"Getting reviews for item: {item_id}, page: {page}")
        
        try:
            response = self._make_request('item_review_2', params)
            reviews_count = len(response.get('result', {}).get('reviews', []))
            self.logger.info(f"Retrieved {reviews_count} reviews")
            return response
            
        except Exception as e:
            self.logger.error(f"item_review_2 failed for item_id '{item_id}': {str(e)}")
            raise
    
    def store_categories(self, 
                         seller_id: str,
                         store_id: str,
                         currency: str = "MXN",
                         region: str = "MX") -> Dict[str, Any]:
        """
        Get categories for a specific AliExpress store
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/store_categories?sellerId=231651707&storeId=1102051418&currency=MXN&region=MX'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            seller_id: Seller ID (e.g., "231651707")
            store_id: Store ID (e.g., "1102051418")
            currency: Currency code (default: "MXN")
            region: Region code (default: "MX")
            
        Returns:
            API response with store categories
        """
        params = {
            'sellerId': str(seller_id),
            'storeId': str(store_id),
            'currency': currency,
            'region': region
        }
        
        self.logger.info(f"Getting categories for store: {store_id}")
        
        try:
            response = self._make_request('store_categories', params)
            categories_count = len(response.get('result', {}).get('categories', []))
            self.logger.info(f"Retrieved {categories_count} store categories")
            return response
            
        except Exception as e:
            self.logger.error(f"store_categories failed for store '{store_id}': {str(e)}")
            raise
    
    def store_info(self, 
                   seller_id: str,
                   currency: str = "MXN",
                   region: str = "MX",
                   locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get information for a specific AliExpress store
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/store_info?sellerId=231651707&currency=MXN&region=MX&locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            seller_id: Seller ID (e.g., "231651707")
            currency: Currency code (default: "MXN")
            region: Region code (default: "MX")
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with store information
        """
        params = {
            'sellerId': str(seller_id),
            'currency': currency,
            'region': region,
            'locale': locale
        }
        
        self.logger.info(f"Getting store info for seller: {seller_id}")
        
        try:
            response = self._make_request('store_info', params)
            store_name = response.get('result', {}).get('storeTitle', 'N/A')
            self.logger.info(f"Retrieved info for store: {store_name}")
            return response
            
        except Exception as e:
            self.logger.error(f"store_info failed for seller '{seller_id}': {str(e)}")
            raise
    
    def item_sku(self, 
                 item_id: str,
                 currency: str = "MXN",
                 region: str = "MX",
                 locale: str = "es_ES") -> Dict[str, Any]:
        """
        Get SKU/variants information for a specific AliExpress item
        
        Equivalent to: curl --request GET 
        --url 'https://aliexpress-datahub.p.rapidapi.com/item_sku?itemId=1005005244562338&currency=MXN&region=MX&locale=es_ES'
        --header 'x-rapidapi-host: aliexpress-datahub.p.rapidapi.com'
        --header 'x-rapidapi-key: YOUR_KEY'
        
        Args:
            item_id: AliExpress item ID (e.g., "1005005244562338")
            currency: Currency code (default: "MXN")
            region: Region code (default: "MX")
            locale: Language locale (default: "es_ES")
            
        Returns:
            API response with item SKU/variants
        """
        params = {
            'itemId': str(item_id),
            'currency': currency,
            'region': region,
            'locale': locale
        }
        
        self.logger.info(f"Getting SKU info for item: {item_id}")
        
        try:
            response = self._make_request('item_sku', params)
            sku_count = len(response.get('result', {}).get('skuInfo', {}).get('skuProps', []))
            self.logger.info(f"Retrieved {sku_count} SKU options")
            return response
            
        except Exception as e:
            self.logger.error(f"item_sku failed for item_id '{item_id}': {str(e)}")
            raise