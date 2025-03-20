from dataclasses import dataclass
 
@dataclass
class Person:
    person_id: str = ""
    person_begin_time: str = ""
 
    def __init__(self, **kwargs):
        # Normaliza ambas formas de person_id
        self.person_id = kwargs.get("person_id") or kwargs.get("personId", "")
        self.person_begin_time = kwargs.get("person_begin_time") or kwargs.get("beginTime", "")