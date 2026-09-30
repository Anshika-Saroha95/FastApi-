from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def hello():
    return{'message':'Hello world'}

@app.get("/about")
def about():
    return{"message":"CampusX is a training platform"}