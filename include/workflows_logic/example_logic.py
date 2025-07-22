# Example business logic from n8n workflows
def process_data(input_data):
    """Convert n8n JavaScript logic to Python"""
    processed = input_data.upper()
    return processed

def validate_api_response(response):
    """Validation logic from n8n workflows"""
    return response.get('status') == 'success'