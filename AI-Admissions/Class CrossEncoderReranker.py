class CrossEncoderReranker:
    def __init__(self, model_name="BAAI/bge-reranker-v2-m3", top_k=3):
        print(f"Đang tải Cross-Encoder Reranker: {model_name}...")
        # Sử dụng CrossEncoder từ thư viện sentence-transformers
        self.model = CrossEncoder(model_name, max_length=512)
        self.top_k = top_k
        print(f" Cross-Encoder Reranker đã sẵn sàng, top_k={top_k}.")

    def rerank(self, query: str, documents: list[Document]) -> list[Document]:
        if not documents:
            return []

        # 1. Ghép cặp Câu hỏi và từng Tài liệu
        pairs = [[query, doc.page_content] for doc in documents]

        # 2. Cross-Encoder chấm điểm dựa trên self-attention toàn phần
        scores = self.model.predict(pairs)

        # 3. Ghép điểm số vào tài liệu tương ứng
        doc_score_pairs = list(zip(documents, scores))

        # 4. Sắp xếp lại danh sách từ điểm cao nhất xuống thấp nhất
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

        # 5. Cắt lấy Top-K tài liệu chất lượng nhất
        return [doc for doc, score in doc_score_pairs[:self.top_k]]
