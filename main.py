import json
import logging
from dto.person_dto import Person
from services.hik_service import get_person_info, edit_person_info
 
if __name__ == "__main__":
    try:
        person_code = '6211765992'
        end_time = '2037-05-26T15:00:00+08:00'
        
        person_data = get_person_info(person_code)
        if 'data' not in person_data:
            logging.error("No person data found.")
            exit(1)
 
        person = Person(**person_data["data"])
        person_update = edit_person_info(person, person_code, end_time)
        
        logging.info("Person update response:")
        logging.info(json.dumps(person_update, indent=4))
        #print(json.dumps(person_update, indent=4))
 
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")