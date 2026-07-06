from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent

from app.core.config import GOOGLE_API_KEY
from app.tools.calculator_tool import  calculator_tool
from app.tools.time_tool import time_tool

class GeminiService:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
        )
        self.agent = create_agent(
            model=self.llm,
            tools=[
                calculator_tool,
                time_tool,
            ],
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an expert AI tutor.

            Explain everything clearly.

            If appropriate, include examples.

            Question:

            {question}
            """
        )

    def ask(self, question: str):

        chain = self.prompt | self.agent

        response = chain.invoke(
            {
                "question": question
            }
        )

        return response