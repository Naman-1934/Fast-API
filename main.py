# Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server that acts as the production-ready 
# engine used to run and serve FastAPI applications

from fastapi import FastAPI, Path, HTTPException, Query
import json


from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal


# Object of FastAPI.
app = FastAPI()


class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=100, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'UnderWeight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'obese'


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:

        # dump data from data dictionay into a file f. r
        json.dump(data, f)


# we use get because we want to get the data from the server.
# when someone visits www.naman.com/ then it will redict to this API.
@app.get("/")
def hello():
    return {'message': "Patient Management System API"}

### uvicorn main:app --reload, in this reload will automatically reload the server when we make a changes 
# and click on a save button.
@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records..'}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = "ID of the patient in the DB", example="P001")):

    # Load all the data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')


########################## Query Parameters ##########################
########################## Sorting and Order by ######################

@app.get('/sort')
### Sort_by is compusory that is why ... is there and order is optional that is why we have given defauly value
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), 
    order: str = Query("asc", description="sort in ascending or descending order")):

    valid_field = ['height', 'weight', 'bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_field}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order select from between asc and desc")


    # Load the data
    data = load_data()

    # if user entered desc then sort_order will be True and if user entered asc then sort_order will be False.
    sort_order = True if order == 'desc' else False

    # if sorted_order is True then it will sort in descending and if it is False then it will sort in ascending.
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# patient is a object as a variable and pydantic model checks whether a given data in a proper format and according to the rules and if it is a correct then it will go further.
@app.post('/create')
def create_patient(patient:Patient):

    # Load Existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient Already exists.')

    # new patient add to the database
    # data in a dictionary format and patient is a pydantic object so, we need to add patient obejct into an existed data
    # We need to convert that patient object into a dictionary

    # model_dump will convert object into a dictionary.
    data[patient.id] = patient.model_dump(exclude=['id'])


    # Save into json file.
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully.'})

