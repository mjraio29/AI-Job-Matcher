import cohere
import os
import json
from dotenv import load_dotenv

load_dotenv()

def score_match(resume_text, job):
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    prompt = f"""You are a job match analyzer. Compare this resume to the job and respond in this exact format:

SCORE: [0-100]
REASONS: [2-3 bullet points why they match]
GAPS: [2-3 skills or experiences missing]

Resume:
{resume_text[:2000]}

Job Title: {job['title']}
Company: {job['company']}
Tags: {', '.join(job.get('tags', []))}
Description: {job['description'][:500]}"""

    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content[0].text

def score_all_jobs(resume_text, jobs_file="jobs/jobs.json"):
    with open(jobs_file) as f:
        jobs = json.load(f)

    results = []
    for i, job in enumerate(jobs[:5]):
        print(f"Scoring job {i+1}/5: {job['title']} at {job['company']}...")
        analysis = score_match(resume_text, job)
        results.append({
            "title": job["title"],
            "company": job["company"],
            "url": job["url"],
            "analysis": analysis
        })

    # Save results
    with open("output/matches.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to output/matches.json")
    return results

if __name__ == "__main__":
    from resume.parser import parse_resume
    from resume.extractor import extract_info

    resume_text = parse_resume("resume/Offical Resume - Michael Raio.docx")
    print("\n--- JOB MATCH RESULTS ---\n")
    results = score_all_jobs(resume_text)
    for r in results:
        print(f"\n{'='*40}")
        print(f"Job: {r['title']} @ {r['company']}")
        print(f"{r['analysis']}")
