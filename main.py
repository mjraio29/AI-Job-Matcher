from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import shutil, os, json
from dotenv import load_dotenv
from resume.parser import parse_resume
from resume.extractor import extract_info
from jobs.scraper import fetch_jobs, save_jobs
from matcher.scorer import score_match
from matcher.cover_letter import generate_cover_letter

load_dotenv()
app = FastAPI(title="AI Job Matcher")

@app.get("/", response_class=HTMLResponse)
def home():
    return open("templates/index.html").read()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    path = f"resume/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = parse_resume(path)
    info = extract_info(text)
    return {"status": "ok", "extracted": info}

@app.get("/search-jobs")
def search_jobs(keyword: str = "python"):
    jobs = fetch_jobs(keyword)
    save_jobs(jobs)
    return {"status": "ok", "count": len(jobs), "jobs": jobs}

@app.post("/score-jobs")
async def score_jobs(file: UploadFile = File(...)):
    path = f"resume/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    resume_text = parse_resume(path)
    with open("jobs/jobs.json") as f:
        jobs = json.load(f)
    results = []
    for job in jobs[:3]:
        analysis = score_match(resume_text, job)
        results.append({"title": job["title"], "company": job["company"], "url": job["url"], "analysis": analysis})
    return {"results": results}

@app.post("/cover-letter")
async def cover_letter(file: UploadFile = File(...), job_index: int = Form(0)):
    path = f"resume/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    resume_text = parse_resume(path)
    with open("jobs/jobs.json") as f:
        jobs = json.load(f)
    job = jobs[job_index]
    letter = generate_cover_letter(resume_text, job)
    return {"job": job["title"], "company": job["company"], "letter": letter}
