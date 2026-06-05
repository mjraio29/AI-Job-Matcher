import requests
import json
import os

def fetch_jobs(keyword="python developer", limit=10):
    print(f"Searching for: {keyword}...")
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # First item is metadata, skip it
    jobs = [j for j in data[1:] if isinstance(j, dict)]

    # Filter by keyword
    keyword_lower = keyword.lower()
    matched = []
    for job in jobs:
        title = job.get("position", "").lower()
        tags = " ".join(job.get("tags", [])).lower()
        desc = job.get("description", "").lower()
        if keyword_lower in title or keyword_lower in tags or keyword_lower in desc:
            matched.append({
                "title": job.get("position", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "Remote"),
                "tags": job.get("tags", []),
                "url": job.get("url", ""),
                "description": job.get("description", "")[:500]
            })
        if len(matched) >= limit:
            break

    print(f"Found {len(matched)} jobs.")
    return matched

def save_jobs(jobs, filename="jobs/jobs.json"):
    with open(filename, "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved to {filename}")

if __name__ == "__main__":
    import sys
    keyword = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "python"
    jobs = fetch_jobs(keyword)
    save_jobs(jobs)
    print("\n--- SAMPLE JOB ---")
    if jobs:
        j = jobs[0]
        print(f"Title: {j['title']}")
        print(f"Company: {j['company']}")
        print(f"Location: {j['location']}")
        print(f"Tags: {', '.join(j['tags'])}")
        print(f"URL: {j['url']}")
