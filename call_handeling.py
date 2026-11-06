from call_function import available_functions, call_function


def start_chat(client, messages, args) -> bool:
    """Handle one model turn, update history, and return whether it is finished."""
    # Calling an API
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )
    # Response handling
    if response.usage is None:
        raise RuntimeError("Failed API request")

    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)

            if result_message is None:
                raise Exception("Tool call results cannot be empty")

            messages.append(result_message)

            if args.verbose:
                print(f"-> {result_message['content']}")
        return False

    print(message.content)
    return True
