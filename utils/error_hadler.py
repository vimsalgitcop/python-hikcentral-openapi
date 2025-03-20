import logging
import requests
 
def handle_request_error(e: requests.exceptions.RequestException, api_path: str):
    logging.error(f"Error in request to {api_path}: {str(e)}")
    return {"error": str(e)}
 
def handle_response_error(response_data, api_path):
    if response_data.get('code') == '2':
        logging.warning(f"Invalid parameters: {response_data.get('msg')}")
    else:
        logging.info(f"Request to {api_path} successful: {response_data}")