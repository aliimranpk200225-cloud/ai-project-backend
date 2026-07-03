from langchain_community.vectorstores import FAISS


class VectorStoreService:

    INDEX_PATH = "faiss_index"

    def create_vector_store(self, chunks, embedding_model):

        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embedding_model
        )

        return vector_store

    def save_vector_store(self, vector_store):

        vector_store.save_local(self.INDEX_PATH)

    def load_vector_store(self, embedding_model):

        return FAISS.load_local(
            self.INDEX_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )