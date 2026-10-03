from pydantic import BaseModel, EmailStr,field_validator
from typing import List, Dict

class Patient(BaseModel):

    name:str
    email:EmailStr
    age:int
    weight:float #kg
    height:float #mtr
    married:bool
    allergies:List[str]
    contact_details: Dict[str,str]

@field_validator('email')
@classmethod
def email_validator(cls,value):
    valid_domains= ['hdfc.com','icici.com']
    # abc@gmail.com
    domain_name = value.split('@')[-1]

    if domain_name not in valid_domains:
        raise ValueError('Not in valid domain')

    return value

@field_validator('name')
@classmethod
def transform_name(cls, value):
    return value.upper()

@field_validator('age',mode='before')
@classmethod
def validate_age(cls,value):
    if 0 < value < 100:
        return value
    else:
        raise ValueError('Age should be in between 0 and 100')



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI',patient.calculate_bmi)
    print('updated') 

patient_info = {'name': 'Arun','email':'abc@gmail.com','linkedIn_url':'http://linkedin.com/123', 'age':'65','weight':64.5,'height':1.72,'married':True,'allergies':['pollen','dust'], 'contact_details':{'phone':'2324345452','emergency':'7653248254'}}

patient1 = Patient(**patient_info)  
update_patient_data(patient1) 