import os
import logging
import getpass
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from app.core.config import settings

from .prompt import competitive_analysis_prompt_text, company_websearch_prompt_text

logger = logging.getLogger("uvicorn")

# Create the agent


MODEL = "gemini-2.5-pro-preview-05-06"


class CompetitorAnalysisAgent:
    def __init__(self):

        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass(
                "Enter API key for Google Gemini: "
            )
        logger.info(f"GOOGLE_API_KEY: {os.environ.get('GOOGLE_API_KEY')}")
        self.model = ChatGoogleGenerativeAI(
            model=MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1,
        )

        self.search = TavilySearchResults(
            max_results=2, api_key=settings.TAVILY_API_KEY
        )
        self.tools = [self.search]
        self.agent_executor = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=competitive_analysis_prompt_text,
        )

    def run(self, company_url: str):
        prompt = company_websearch_prompt_text.format(company_url=company_url)
        logger.info(f"Prompt: {prompt}")
        return self.agent_executor.invoke({"messages": [HumanMessage(content=prompt)]})
