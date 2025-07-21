import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    args = sys.argv
    if len(args) < 2:
        print("Please provide command line argument for the prompt.")
        sys.exit(1)

    
    model_name = 'gemini-2.0-flash-001'

    messages = [
        types.Content(role="user", parts=[types.Part(text=args[1])]),
    ]

    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    print(response.text)
    if "--verbose" in args:
        print(f"User prompt: {args[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()