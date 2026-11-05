import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("Open router API-key not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# User arguments parser
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

# Calling an API
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ],
)

if response.usage is None:
    raise RuntimeError("Failed API request")

prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens

print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {completion_tokens}")
print(response.choices[0].message.content)
