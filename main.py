# Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server that acts as the production-ready 
# engine used to run and serve FastAPI applications

from fastapi import FastAPI


# Object of FastAPI.
app = FastAPI()


# we use get because we want to get the data from the server.
# when someone visits www.naman.com/ then it will redict to this API.
@app.get("/")
def hello():
    return {'message': "Hello, from naman"}

### uvicorn main:app --reload, in this reload will automatically reload the server when we make a changes 
# and click on a save button.
@app.get("/education")
def education():
    return {'message': "I have completed my graduation in Computer Engineering from Vadodara Institute of Engineering. In May 2026, completed my M.Tech in Computer Engineering from the Parul University."}

@app.get("/skills")
def skills():
    return {'message': "I have skills in Python, SQL, MS Excel, MS Office, Powe BI, Tableau, Machine Learning, Tensorflow and basic knowledge of Transformers, NLP."}

@app.get("/contact me")
def contact_me():
    return {'message': "You can contact me on my email: xyz@gmail.com and also contact me on my Phone number: 1234567890. You can reach out me through linkedin message. "}

@app.get("/about")
def about():
    return {'message': 'This website is a a PortFolio Website, as a data analyst whose gonna be an AI Developer in future but currently i am learning a fast-api then move to the ai-application developer.'}
