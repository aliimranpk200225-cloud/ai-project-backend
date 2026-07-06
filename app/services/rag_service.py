from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from operator import itemgetter




#examples of runable lambda func
# also RunnableParallel
# ✅ RunnableBranch
# ✅ RunnableAssign
# ✅ RunnableSequence  examples need to be practised
def capitalize(text):
    return text.upper()

def add_exclamation(text):
    return text + "!"

from langchain_core.runnables import RunnableLambda

add_exclamation = RunnableLambda(add_exclamation)






class RAGService:

    def __init__(self, retriever, llm):

        self.retriever = retriever
        self.llm = llm

    def build_chain(self):

        prompt = ChatPromptTemplate.from_template(
            """
        You are a helpful assistant.
        

        Use ONLY the context below.
        if question is not in text below then dont answer it  its very important.
        Previous Conversation:

        {history}

        Context:
        {context}

        Question:
        {question}
        """
        )

        chain = (
                {
                    "context": itemgetter("question") | self.retriever,
                    "question": itemgetter("question"),
                    "history": itemgetter("history"),
                }
                | prompt
                | self.llm

        )

        return chain