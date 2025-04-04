import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as gen_ai
from browser_use import Agent, Browser, BrowserConfig
from pydantic import SecretStr

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_ALT")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Please set it in your .env file.")

# Ensure arguments are passed
if len(sys.argv) < 3:
    print("Usage: python script.py '<global_task>' '<output_file>'")
    sys.exit(1)

global_task = sys.argv[1]  # First argument is the task
output_file = sys.argv[2]  # Second argument is the output filename

browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    )
)

model = gen_ai.GenerativeModel("gemini-2.0-flash-exp")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key).get_secret_value())

task_llm = "Create a concise step-by-step task as a prompt which can be given to an LLM to complete the following task:"

def TaskLLM(global_task: str, task_llm: str) -> str:
    prompt = (
        f"{task_llm} The task is: {global_task}.\n\n"
        "Specify which buttons/elements to click. Format the response as a numbered step-by-step list like this:\n"
        "1. [First step]\n"
        "2. [Second step]\n"
        "3. [Third step]\n"
        "...\n"
        "Ensure clarity and precision in each step."
    )

    response = model.generate_content(prompt)
    
    if hasattr(response, "text"):
        return response.text
    elif isinstance(response, str):  
        return response  
    else:
        raise ValueError("Unexpected response format from Gemini API.")

async def run_agent():
    try:
        agent = Agent(task=TaskLLM(global_task, task_llm), llm=llm, browser=browser)
        result = await agent.run()
        return result
    except Exception as e:
        print(f"Error running agent: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(run_agent())