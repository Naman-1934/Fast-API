from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd


##### Import the ml model
with open('demo_model.pkl', 'rb') as f:
    model = pickle.load(f)


### FastAPI app object
app = FastAPI()

tier_l_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal","Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

##### pydantic model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")] 
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the user")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual Salary of the user in lpa")]
    smoker: Annotated[bool, Field(..., description="Is user a smoker")]
    city: Annotated[str, Field(..., description="The city that the user belongs to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., gt=0, lt=120, description="Occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "Young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle-aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_l_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post('/predict')
# User's data is which type of object? = UserInput object and it is our pydantic model also.
def predict_premium(data: UserInput):

    # We need to pass one row of data and in that row we will pass dictionary
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])


    ##### Now, we will call predict function which will be created above.
    prediction = model.predict(input_df)[0]


    #### We will return this prediction into a json format.