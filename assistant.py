# from open ai cookbook:
# https://cookbook.openai.com/examples/assistants_api_overview_python

from openai import OpenAI
from dotenv import load_dotenv
import os
import time
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

isDelayed = True

client = OpenAI(api_key=api_key)

#step 1 - create an assistant
assistant = client.beta.assistants.create(
    name = "math tutor",
    instructions = "You are a personal math tutor. Write and run code to answer math questions.",
    tools = [{"type": "code_interpreter"}],
    model = "gpt-4o"
)
if isDelayed:
    time.sleep(2)
#step 2 - create a thread
thread = client.beta.threads.create()
print(thread)

#step 3 - add a message to the thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "Solve this problem: 3x + 11 = 14"
)
if isDelayed:
    time.sleep(2)
#step 4 - run the assistant
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)
if isDelayed:
    time.sleep(2)
#step 5 - display the assistant's response
run = client.beta.threads.runs.retrieve(
    thread_id = thread.id, 
    run_id = run.id
)
if isDelayed:
    time.sleep(1)
messages = client.beta.threads.messages.list(
    thread_id = thread.id
)
if isDelayed:
    time.sleep(1)
for message in reversed(messages.data): 
    print(message.role + ": " + message.content[0].text.value)

