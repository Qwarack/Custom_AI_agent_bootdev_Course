import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions
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

# Calling an API
response = client.chat.completions.create(
    model="openrouter/free", messages=messages, temperature=0, tools=available_functions
)

if response.usage is None:
    raise RuntimeError("Failed API request")


prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

message = response.choices[0].message
if message.tool_calls is not None:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
else:
    print(message.content)
