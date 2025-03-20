import requests
import logging
from utils.signature import generate_signature
from utils.error_hadler import handle_request_error, handle_response_error
from utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hikcentral_api.log"),
        logging.StreamHandler()
    ]
)
 
def make_request(method: str, api_path: str, payload: dict = None):
    url = f"{Config.HIKCENTRAL_IP}{api_path}"
    signature, timestamp = generate_signature(method, api_path)
    
    headers = {
        "Content-Type": "application/json",
        "X-Ca-Key": Config.APP_KEY,
        "x-ca-signature": signature,
        "TimeStamp": timestamp
    }
 
    try:
        response = requests.request(method, url, json=payload, headers=headers, verify=False, timeout=10)
        response_data = response.json()
        handle_response_error(response_data, api_path)
        return response_data
    except requests.exceptions.RequestException as e:
        return handle_request_error(e, api_path)
 
def get_hikcentral_version():
    return make_request("POST", "/artemis/api/common/v1/version")
 
def get_person_info(person_code):
    return make_request("GET", f"/artemis/api/resource/v1/person/personCode/personInfo", payload={"personCode": person_code})
 
def edit_person_info(person, person_code, end_time):
    payload = {
        "personId": person.person_id,
        "personCode": person_code,
        "beginTime": person.person_begin_time,
        "endTime": end_time,
    }
    return make_request("POST", "/artemis/api/resource/v1/person/single/update", payload=payload)