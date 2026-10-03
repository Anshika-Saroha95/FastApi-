from pydantic import BaseModel, EmailStr,AnyUrl,Field
from typing import List,Optional, Annotated 


#type validation--------
class Patient(BaseModel):

    # defining ideal schema---
    # What a function needs name and age (also we have to perform type validation)

    # name: str = Field(max_length=50)
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars',examples=['Nitish','Amit'])]
    email:EmailStr
    linkedIn_url: AnyUrl

    age:int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    # married: bool
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Optional[list[str]] = None  
    contact_details: dict[str, str]


def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name': 'Arun','email':'abc@gmail.com','linkedIn_url':'http://linkedin.com/123', 'age':'30','weight':64.5,'married':True,'allergies':['pollen','dust'], 'contact_details':{'phone':'2324345452'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)