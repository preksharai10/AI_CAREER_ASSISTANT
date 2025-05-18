# AI-Powered Career Assistant
This project is an AI-powered career assistant that analyzes resumes and provides personalized career guidance using Google's Gemini API. The application is built with:

- **FastAPI** backend serving API endpoints for resume analysis and career options.
- **Streamlit** frontend providing an interactive UI that calls FastAPI APIs.

---

## Features

- Upload your resume (PDF or DOCX).
- Select a career goal from dynamically fetched tech career options.
- Receive a detailed career analysis, skill gap identification, and a personalized 4-week learning plan.
- Download your career plan as a PDF.

---

## Architecture

- **FastAPI Backend:**  
  - Exposes `/career_options/` endpoint to get career options using Gemini API.  
  - Exposes `/analyze/` endpoint to analyze resumes with Gemini, extracting text from PDF/DOCX files.  
  - Handles CORS to allow Streamlit frontend access.

- **Streamlit Frontend:**  
  - Fetches career options from FastAPI backend.  
  - Uploads resume and sends it along with selected career goal to backend for analysis.  
  - Displays Gemini-generated career plan.  
  - Allows downloading the plan as PDF.
 ## How to Run Locally

1. Clone the repo.

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Create a .env file with your Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```
5. Run FastAPI backend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

6. Run Streamlit frontend (in another terminal):

```bash
streamlit run app.py
