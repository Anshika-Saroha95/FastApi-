from fastapi import FastAPI, Path, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

from pathlib import Path as FilePath
import json


app = FastAPI(title="Patient Management System API")


# Project directories
BASE_DIR = FilePath(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
DATA_FILE = BASE_DIR / "patient.json"


# Static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


# Patient Model
class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["male", "female", "others"], Field(...)]
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"

        elif self.bmi < 25:
            return "Normal"

        elif self.bmi < 30:
            return "Overweight"

        else:
            return "Obese"


# Patient Update Model
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# Load Data
def load_data():

    if not DATA_FILE.exists():
        return {}

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    return data


# Save Data
def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# FRONTEND ROUTE
@app.get("/")
@app.get("/app")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# API HOME
@app.get("/api")
def hello():

    return {"message": "Patient Management System API"}


@app.get("/about")
def about():

    return {
        "message": "Fully functional API to manage your patient records"
    }


# VIEW ALL PATIENTS
@app.get("/view")
def view():

    data = load_data()

    return data


# VIEW SINGLE PATIENT
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the DB",
        examples=["P001"]
    )
):

    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# SORT PATIENTS
@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="Sort by height, weight or BMI"),
    order: str = Query("asc", description="Ascending or descending order")
):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select between asc and desc"
        )

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data


# CREATE PATIENT
@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )

    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully"}
    )


# UPDATE PATIENT
@app.put("/edit/{patient_id}")
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate
):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id

    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(
        exclude={"id"}
    )

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient updated successfully"}
    )


# DELETE PATIENT
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    del data[patient_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully"}
    )