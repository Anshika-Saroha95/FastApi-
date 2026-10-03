from pydantic import BaseModel, EmailStr,model_validator
from typing import List, Dict

class Patient(BaseModel):

    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:List[str]
    contact_details: Dict[str,str]

    @classmethod
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patient older than 60 must have an emergency contact')
        return model



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated') 

patient_info = {'name': 'Arun','email':'abc@gmail.com','linkedIn_url':'http://linkedin.com/123', 'age':'65','weight':64.5,'married':True,'allergies':['pollen','dust'], 'contact_details':{'phone':'2324345452','emergency':'7653248254'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)    