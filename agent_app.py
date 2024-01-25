from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

import pandas as pd
import io
import os

from prompts import PROMPT

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_agent(file_buffer: io.BytesIO, file_type: str) -> AgentExecutor:
    """
    Create data agent from an uploaded file.

    Args:
        file_buffer: BytesIO object of the uploaded file.
        file_type: Type of the file ('csv' or 'excel').

    Returns:
        An agent executor.
    """
    llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY, 
    model="gpt-4",
    temperature=0.1,
    )

    if file_type == 'csv':
        df = pd.read_csv(file_buffer)
    elif file_type == 'excel':
        df = pd.read_excel(file_buffer)
    else:
        raise ValueError("Unsupported file type")
    
    return create_pandas_dataframe_agent(llm, df, verbose=True)

def query_agent(agent: AgentExecutor, query: str) -> str:
    """Query an agent and return the response."""
    prompt = PromptTemplate(template=PROMPT, input_variables=["query"])
    return agent.run(prompt.format(query=query))
