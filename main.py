import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_handeling import start_chat
from prompts import system_prompt

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
# add verbose parser argument
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


# Storing messages for context
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):
    if start_chat(client=client, messages=messages, args=args):
        break
else:
    print("Maximum of 20 iterations reached without a final response.")
    raise SystemExit(1)
