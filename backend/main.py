
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to AI Study Notes Generator"}

@app.get("/about")
def about():
    return {
        "project": "AI Study Notes Generator",
        "version": "1.0",
        "developer": "Mahek J"
    }