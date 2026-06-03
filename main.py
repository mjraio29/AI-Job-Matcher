from dotenv import load_dotenv
import os

load_dotenv()

def check_setup():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key or key == "your_api_key_here":
        print("❌  ANTHROPIC_API_KEY not set.")
        return False
    print("✅  Setup looks good! API key loaded.")
    return True

if __name__ == "__main__":
    check_setup()
