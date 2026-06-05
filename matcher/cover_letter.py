import cohere
import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_cover_letter(resume_text, job):
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    prompt = f"""Write a professional, personalized cover letter for this job application.
Use the candidate's real experience from the resume. Keep it to 3 paragraphs.
Do not use placeholders — write it as if you are the candidate.

Resume:
{resume_text[:2000]}

Job Title: {job['title']}
Company: {job['company']}
Description: {job['description'][:500]}"""

    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content[0].text

if __name__ == "__main__":
    from resume.parser import parse_resume
    import sys

    resume_text = parse_resume("resume/Offical Resume - Michael Raio.docx")

    # Load first job from jobs.json
    with open("jobs/jobs.json") as f:
        jobs = json.load(f)

    job_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    job = jobs[job_index]

    print(f"Generating cover letter for: {job['title']} @ {job['company']}\n")
    letter = generate_cover_letter(resume_text, job)
    print(letter)

    # Save it
    filename = f"output/cover_letter_{job_index}.txt"
    with open(filename, "w") as f:
        f.write(f"Cover Letter for: {job['title']} @ {job['company']}\n\n")
        f.write(letter)
    print(f"\nSaved to {filename}")
