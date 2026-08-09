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


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI()


# ============================================================
# ENABLE CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STATIC FILES AND TEMPLATES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# UPLOAD FOLDER
# ============================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ============================================================
# ABOUT
# ============================================================

@app.get("/about")
def about():

    return {
        "project": "AI Study Notes Generator",
        "version": "1.1",
        "developer": "Mahek J"
    }


# ============================================================
# COURSE
# ============================================================

@app.get("/course")
def course():

    return {
        "course": "CSE-AIML"
    }


# ============================================================
# SPLIT PDF INTO PAGE CHUNKS
# ============================================================

def split_pdf_into_chunks(doc, pages_per_chunk=8):

    chunks = []

    current_chunk = []

    for page_number, page in enumerate(doc, start=1):

        page_text = page.get_text()

        if page_text.strip():

            page_content = (
                f"\n\n--- PAGE {page_number} ---\n\n"
                f"{page_text}"
            )

            current_chunk.append(page_content)

        if len(current_chunk) == pages_per_chunk:

            chunks.append(
                "\n".join(current_chunk)
            )

            current_chunk = []

    if current_chunk:

        chunks.append(
            "\n".join(current_chunk)
        )

    return chunks


# ============================================================
# GENERATE NOTES FOR ONE CHUNK
# ============================================================

def generate_notes_for_chunk(
    chunk,
    chunk_number,
    total_chunks
):

    prompt = f"""
You are an expert college teacher.

You are creating detailed study notes from section
{chunk_number} of {total_chunks} of a larger PDF.

Create COMPLETE and DETAILED study notes.

IMPORTANT RULES:

1. Do not make the notes extremely short.
2. Preserve important information from the source.
3. Explain technical concepts clearly.
4. Include definitions.
5. Include important concepts.
6. Include examples when present.
7. Include formulas when present.
8. Include advantages and disadvantages when present.
9. Include applications when present.
10. Include important lists.
11. Do not invent information that is not in the PDF.
12. Use headings and subheadings.
13. Use bullet points where appropriate.
14. Mention the relevant page numbers.
15. Make the notes useful for semester exam preparation.

Use this structure when appropriate:

## Topic

### Definition

### Explanation

### Important Concepts

- Point
- Point
- Point

### Examples

### Advantages

### Disadvantages

### Applications

### Exam Points

At the end:

### Section Summary

Give a useful summary of the section.

SOURCE CONTENT:

{chunk}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# UPLOAD PDF
# ============================================================

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    try:

        # ----------------------------------------------------
        # SAVE PDF
        # ----------------------------------------------------

        safe_filename = os.path.basename(
            file.filename
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            safe_filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # ----------------------------------------------------
        # OPEN PDF
        # ----------------------------------------------------

        doc = fitz.open(file_path)


        # ----------------------------------------------------
        # CHECK NUMBER OF PAGES
        # ----------------------------------------------------

        total_pages = len(doc)


        # ----------------------------------------------------
        # SPLIT PDF INTO PAGE CHUNKS
        # ----------------------------------------------------

        chunks = split_pdf_into_chunks(
            doc,
            pages_per_chunk=8
        )


        # ----------------------------------------------------
        # CLOSE PDF
        # ----------------------------------------------------

        doc.close()


        # ----------------------------------------------------
        # CHECK FOR TEXT
        # ----------------------------------------------------

        if len(chunks) == 0:

            return {
                "error": (
                    "No readable text was found in this PDF. "
                    "The PDF may contain scanned images or "
                    "text stored inside images."
                )
            }


        # ----------------------------------------------------
        # GENERATE NOTES
        # ----------------------------------------------------

        all_notes = []

        total_chunks = len(chunks)

        for chunk_number, chunk in enumerate(
            chunks,
            start=1
        ):

            notes = generate_notes_for_chunk(
                chunk,
                chunk_number,
                total_chunks
            )

            all_notes.append(notes)


        # ----------------------------------------------------
        # COMBINE NOTES
        # ----------------------------------------------------

        final_notes = "\n\n".join(
            all_notes
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "message": "Study notes generated successfully!",
            "filename": safe_filename,
            "total_pages": total_pages,
            "chunks_processed": total_chunks,
            "notes": final_notes
        }


    except Exception as e:

        return {
            "error": str(e)
        }