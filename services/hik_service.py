from concurrent.futures import ThreadPoolExecutor, as_completed
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
    return make_request("GET", "/artemis/api/resource/v1/person/personCode/personInfo", payload={"personCode": person_code})

### Set search condition to search the specified person, and fuzzy search is supported
def get_person_list(pageNo, pageSize):
    payload = payload = {
        "pageNo": pageNo,
        "pageSize": pageSize
}
    
    response = make_request("POST", "/artemis/api/resource/v1/person/advance/personList", payload=payload)
    return response

def edit_person_info(person_id, person_code, begin_time, end_time):
    payload = {
        "personId": person_id,
        "personCode": person_code,
        "beginTime": begin_time,
        "endTime": end_time,
    }
    return make_request("POST", "/artemis/api/resource/v1/person/single/update", payload=payload)

def bulk_edit_person_info(person_data, max_workers=10):
    results = {}
    if not isinstance(person_data, list):
        logging.error("Expected person_data to be a list")
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_person = {
            executor.submit(edit_person_info, data['personId'], data['person_code'], data['beginTime'], data['end_time']): data['person_code']
            for data in person_data if isinstance(data, dict)
        }
        
        for future in as_completed(future_to_person):
            person_code = future_to_person[future]
            try:
                results[person_code] = future.result()
            except Exception as e:
                logging.error(f"Error al editar información de la persona {person_code}: {e}")
                results[person_code] = None

    return results
