from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import GOOGLE_API_KEY


class GeminiService:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
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

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "question": question
            }
        )

        return response.content