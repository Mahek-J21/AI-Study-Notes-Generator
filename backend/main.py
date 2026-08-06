from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
import fitz
from groq import Groq
from dotenv import load_dotenv

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------
# Create FastAPI App
# ----------------------------
app = FastAPI()

# ----------------------------
# Enable CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Static Files & Templates
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ----------------------------
# Upload Folder
# ----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------
# Home Page
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
    

# ----------------------------
# About
# ----------------------------
@app.get("/about")
def about():
    return {
        "project": "AI Study Notes Generator",
        "version": "1.0",
        "developer": "Mahek J"
    }

# ----------------------------
# Upload PDF
# ----------------------------
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    prompt = f"""
You are an expert teacher.

Convert the following PDF into clean study notes.

Include:
- Title
- Headings
- Bullet Points
- Important Concepts
- Short Summary

Text:
{text}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        notes = response.choices[0].message.content

        return {
            "message": "Study notes generated successfully!",
            "filename": file.filename,
            "notes": notes
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ----------------------------
# Course
# ----------------------------
@app.get("/course")
def course():
    return {
        "course": "CSE-AIML"
    }