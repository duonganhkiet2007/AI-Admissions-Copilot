class HybridVectorDB:
    def __init__(self, documents, embedding, collection_name="uit_admissions_advanced"):
        self.embedding = embedding
        self.documents = documents

        # Build Vector DB
        print("Đang khởi tạo Vector Database...")
        self.vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding,
            collection_name=collection_name
        )

        # Build BM25 Index
        print("Đang khởi tạo Keyword Index (BM25)...")
        tokenized_docs = [word_tokenize(doc.page_content.lower()) for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs) if documents else None

    def get_retriever(self, search_kwargs: dict = None):
        search_kwargs = search_kwargs or {}
        k = search_kwargs.get("k", 7)
        rrf_k = search_kwargs.get("rrf_k", 40) # Extract rrf_k from search_kwargs
        return HybridRetriever(
            vector_db=self.vector_db,
            bm25=self.bm25,
            documents=self.documents,
            k=k,
            rrf_k=rrf_k # Pass rrf_k to HybridRetriever
        )
