from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
from docx import Document
import io
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global cache for career options
career_options_cache = []

@app.get("/career_options/")
def get_career_options():
    """
    Endpoint to get a dynamic list of career options using Gemini.
    """
    global career_options_cache
    if career_options_cache:
        return {"career_options": career_options_cache}

    prompt = """
List 20 diverse and relevant career paths in the tech industry for aspiring professionals.
Only return the list as bullet points with no explanation or intro.
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Extract and clean each bullet point line
        lines = [
            line.lstrip("•*- ").strip()
            for line in response.text.strip().split("\n")
            if line.strip()
        ]

        career_options_cache = lines
        return {"career_options": lines}
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to fetch career options: {e}"},
            status_code=500
        )

@app.post("/analyze/")
async def analyze_resume(file: UploadFile = File(...), career_goal: str = Form(...)):
    """
    Endpoint to analyze uploaded resume and provide career guidance using Gemini.
    """
    contents = await file.read()
    filename = file.filename.lower()
    text = ""

    # Extract text from PDF or DOCX
    try:
        if filename.endswith(".pdf"):
            with fitz.open(stream=contents, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        elif filename.endswith(".docx"):
            docx_file = io.BytesIO(contents)
            document = Document(docx_file)
            for para in document.paragraphs:
                text += para.text + "\n"
        else:
            return JSONResponse(
                content={"error": "Unsupported file format. Please upload PDF or DOCX."},
                status_code=400,
            )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

    # Gemini Prompt
    prompt = f"""
You are a career assistant AI.

Resume:
{text}

Career Goal: {career_goal}

Please provide a well-structured career analysis in markdown format, covering:

1. **Full Name**
2. **Skills and Experience Summary**
3. **Skills Found in Resume** (technical + soft skills)
4. **Missing Skill Gaps** for the chosen goal
5. A **Personalized 4-week Learning Plan**
6. **Top 5 Free or Affordable Online Courses**
7. Suggest a **More Suitable Career** if resume is misaligned
8. **Top 5 Companies** hiring for this career
9. **Common Job Titles** in this field
"""

    # Call Gemini for analysis
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return JSONResponse(content={"response": response.text})
    except Exception as e:
        return JSONResponse(
            content={"error": f"Gemini error: {e}"},
            status_code=500
        )
