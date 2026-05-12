class SemanticChunker:
    def __init__(self, embedding_model, breakpoint_threshold: float = 0.5, overlap_size: int = 1000):
        self.embeddings = embedding_model
        self.breakpoint_threshold = breakpoint_threshold
        self.overlap_size = overlap_size
        self.min_chunk_size = 1000
        self.max_chunk_size = 5000

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = sent_tokenize(text)
        return [s.strip() for s in sentences if s.strip() and len(s) > 20]

    def _calculate_cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    def _chunk_by_semantic_similarity(self, sentences: List[str]) -> List[str]:
        if not sentences: return []

        sentence_embeddings = self.embeddings.embed_documents(sentences)
        chunks, current_chunk = [], [sentences[0]]

        for i in range(1, len(sentences)):
            prev_emb = sentence_embeddings[i-1]
            curr_emb = sentence_embeddings[i]
            similarity = self._calculate_cosine_similarity(prev_emb, curr_emb)

            chunk_text = " ".join(current_chunk)
            chunk_len = len(chunk_text)

            if chunk_len >= self.max_chunk_size:
                chunks.append(chunk_text)
                current_chunk = [sentences[i]]
            elif similarity >= self.breakpoint_threshold or chunk_len < self.min_chunk_size:
                current_chunk.append(sentences[i])
            else:
                chunks.append(chunk_text)
                current_chunk = [sentences[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def split(self, documents) -> List:
        all_chunks = []
        for doc in tqdm(documents, desc="Semantic chunking"):
            sentences = self._split_into_sentences(doc.page_content)
            if not sentences: continue

            chunks = self._chunk_by_semantic_similarity(sentences)
            for idx, chunk_text in enumerate(chunks):
                if not chunk_text.strip(): continue
                if idx > 0 and self.overlap_size > 0:
                    prev_chunk = chunks[idx-1]
                    # Ensure prev_chunk is a string and has enough length for slicing
                    if isinstance(prev_chunk, str) and len(prev_chunk) >= self.overlap_size:
                        chunk_text = prev_chunk[-self.overlap_size:] + " " + chunk_text

                all_chunks.append(Document(page_content=chunk_text, metadata=doc.metadata.copy()))
        return all_chunks
