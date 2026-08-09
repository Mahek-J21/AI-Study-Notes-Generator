# 📚 AI Study Notes Generator

An AI-powered web application that converts PDF study materials into clean, structured study notes using Generative AI.

## 📌 Project Overview

The AI Study Notes Generator helps students quickly understand and revise study materials.

Users can upload a PDF document, and the application extracts the text from the PDF and uses Generative AI to generate well-structured study notes containing:

- Title
- Headings
- Bullet points
- Important concepts
- Short summary

## ✨ Features

- 📄 Upload PDF documents
- 🤖 AI-powered study note generation
- 📝 Structured and easy-to-read notes
- 📚 Automatic PDF text extraction
- 🌐 Web-based user interface
- ⚡ FastAPI backend
- 🔐 API key stored securely using environment variables

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn

### AI
- Groq API
- Llama 3.3 70B

### PDF Processing
- PyMuPDF

### Other Libraries
- python-dotenv
- Jinja2
- python-multipart

## 📂 Project Structure

```text
AI-Study-Notes-Generator/
│
├── backend/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── uploads/
│
├── screenshots/
│
├── .gitignore
└── README.md