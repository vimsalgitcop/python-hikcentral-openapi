import json
import logging
from services.hik_service import get_person_list, bulk_edit_person_info

# JSON externo
external_data = [ 
    {
        "person_code": "6314504857",
        "end_time": "2037-05-26T15:00:00+08:00"
    },
    {
        "person_code": "6039425213",
        "end_time": "2037-05-26T15:00:00+08:00"
    },
    {
        "person_code": "6022766443",
        "end_time": "2037-05-26T15:00:00+08:00"
    },
    {
        "person_code": "6211765992",
        "end_time": "2037-05-26T15:00:00+08:00"
    }
]


if __name__ == "__main__":
    try:
        # Obtener la lista de personas
        person_update = get_person_list(1, 500)
        person_list = person_update.get("data", {}).get("list", [])
        # Crear un diccionario para el JSON externo para una búsqueda rápida
        external_dict = {item["person_code"]: item["end_time"] for item in external_data}

        # Crear la nueva lista con los datos combinados
        combined_data = [
            {
                "personId": person["personId"],
                "person_code": person["personCode"],
                "beginTime": person["beginTime"],
                "end_time": external_dict.get(person["personCode"], person["endTime"])
            }
            for person in person_list if person["personCode"] in external_dict
        ]

        # Convertir la lista combinada a JSON
        combined_json = json.dumps(combined_data, indent=4)
        # Ejecutar ediciones concurrentes
        results = bulk_edit_person_info(combined_data)
        print(json.dumps(results, indent=4))

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")


