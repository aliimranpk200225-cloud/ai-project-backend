

class RetrieverService:

    def create_retriever(self, vector_store):

        return vector_store.as_retriever(
            search_kwargs={"k": 3}
        )