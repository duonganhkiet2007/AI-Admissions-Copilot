class HybridRetriever(BaseRetriever):
    vector_db: Any = Field(description="Chroma Vector DB")
    bm25: Any = Field(description="BM25 Index")
    documents: List = Field(description="List of all chunks")
    k: int = 7
    rrf_k: int = 40

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        results_list = []

        # 1. Lấy kết quả từ Vector Search (Ngữ nghĩa)
        vector_results = self.vector_db.similarity_search(query, k=self.k)
        results_list.append(vector_results)

        # 2. Lấy kết quả từ BM25 Search (Từ khóa chính xác)
        if self.bm25 is not None:
            tokenized_query = word_tokenize(query.lower())
            bm25_scores = self.bm25.get_scores(tokenized_query)
            top_k_indices = np.argsort(bm25_scores)[::-1][:self.k]
            bm25_results = [self.documents[i] for i in top_k_indices]
            results_list.append(bm25_results)

        # 3. Kết hợp bằng thuật toán Reciprocal Rank Fusion (RRF)
        return self._reciprocal_rank_fusion(results_list, k=self.rrf_k)[:self.k]

    def _reciprocal_rank_fusion(self, results_list: List[List], k: int) -> List[Document]:
        rrf_scores = defaultdict(float)
        doc_content_map = {}

        for results in results_list:
            for rank, doc in enumerate(results, start=1):
                doc_id = doc.page_content
                rrf_scores[doc_id] += 1 / (k + rank)
                doc_content_map[doc_id] = doc

        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_content_map[doc_id] for doc_id, score in sorted_docs]
