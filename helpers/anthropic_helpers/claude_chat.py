import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))

def chat_with_claude(messages_arr, system_prompt):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0,
        system=system_prompt,
        messages=messages_arr,
    )
    return message