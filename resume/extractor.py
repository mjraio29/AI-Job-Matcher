import cohere
import os
from dotenv import load_dotenv
from resume.parser import parse_resume

load_dotenv()

def extract_info(resume_text):
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    response = co.chat(
        model="command-a-03-2025",
        messages=[
            {
                "role": "user",
                "content": f"Extract from this resume:\n1. SKILLS\n2. EXPERIENCE\n3. EDUCATION\n\nResume:\n{resume_text[:3000]}"
            }
        ]
    )
    return response.message.content[0].text

if __name__ == "__main__":
    text = parse_resume("resume/Offical Resume - Michael Raio.docx")
    if text:
        print("Extracting info with AI...\n")
        result = extract_info(text)
        print(result)
