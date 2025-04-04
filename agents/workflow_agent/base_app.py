import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as gen_ai
from browser_use import Agent, Browser, BrowserConfig, Controller
from typing import List
from pydantic import BaseModel, SecretStr

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_ALT")

# Browser Setup
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)

# LLM Setup
model = gen_ai.GenerativeModel("gemini-2.0-flash-exp")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

async def run_agent(task):
    """Runs the appropriate agent based on DeepSearch setting."""
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        use_vision_for_planner=True
    )
    
    result = await agent.run()
    return result

def enhancePrompt(global_task):
    prompt = (
        "Create a concise step-by-step task as a prompt which can be given to an LLM to complete the following task:" 
        f"The task is: {global_task}.\n\n"
        "Specify which buttons/elements to click. Format the response as a numbered step-by-step list like this:\n"
        "1. [First step]\n"
        "2. [Second step]\n"
        "3. [Third step]\n"
        "...\n"
        "Ensure clarity and precision in each step. The output that you extract must me in points and plain text."
    )

    response = model.generate_content(prompt)
    
    if hasattr(response, "text"):
        return response.text
    elif isinstance(response, str):  
        return response  
    else:
        raise ValueError("Unexpected response format from Gemini API.")

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Streamlit App UI
st.title("AI Agent Controller")
st.write("Enter a task for the AI agent to execute.")

task_input = st.text_area("Task:", "Go to hacker news and fetch the first 5 posts.")
enhanced_prompt = enhancePrompt(task_input)

if st.button("Run Agent"):
    st.write("Running agent... Please wait ⏳")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run_agent(enhanced_prompt))