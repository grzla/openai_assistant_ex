#not working - no async endpoints
# 
from dotenv import load_dotenv
import os
import asyncio
from openai import OpenAI
import json

load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

def show_json(obj):
    display(json.loads(obj.model_dump_json()))


client = OpenAI(api_key=api_key)

async def main():
    # step 1 - create an assistant
    assistant = await client.beta.assistants.create(
        name="math tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o"
    )

    # step 2 - create a thread
    thread = await client.beta.threads.create()
    print(thread)

    # step 3 - add a message to the thread
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Solve this problem: 3x + 11 = 14"
    )

    # step 4 - run the assistant
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # step 5 - display the assistant's response
    run = await client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)

asyncio.run(main())