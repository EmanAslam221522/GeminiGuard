import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Configure Gemini using environment variable
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    print("Simple LLM Demo - No SQL, just pure language model")
    print("Type 'exit' to quit")
    
    while True:
        prompt = input("\nEnter your prompt: ")
        if prompt.lower() == 'exit':
            break
            
        response = model.generate_content(prompt)
        print(f"\nResponse: {response.text}")

if __name__ == "__main__":
    main()
