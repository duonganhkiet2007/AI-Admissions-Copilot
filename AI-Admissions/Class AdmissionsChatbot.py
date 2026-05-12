class AdmissionsChatbot:
    def __init__(self, llm, retriever, internal_vdb, embeddings):
        self.llm = llm
        self.retriever = retriever
        self.internal_vdb = internal_vdb
        self.embeddings = embeddings
        self.tavily_tool = TavilySearchResults(max_results=3)

        self.prompt_template = """<|im_start|>system
Bạn là trợ lý ảo UIT. Bạn có hai nguồn dữ liệu: [NỘI BỘ] (về UIT) và [INTERNET] (về xã hội).

QUY TẮC:
1. Nếu câu hỏi về UIT: Dùng [NỘI BỘ].
2. Nếu câu hỏi về đời sống/giá cả (như giá xăng): Dùng [INTERNET].
3. Trích dẫn nguồn cụ thể nếu dùng dữ liệu Internet.
4. Nếu cả hai nguồn không có thông tin, hãy báo là không biết, đừng bịa đặt.<|im_end|>
<|im_start|>user
[DỮ LIỆU NỘI BỘ]: {internal_context}
[DỮ LIỆU INTERNET]: {web_context}
[CÂU HỎI]: {question}<|im_end|>
<|im_start|>assistant
"""
        self.prompt = PromptTemplate.from_template(self.prompt_template)
        self.chain = self.prompt | self.llm | StrOutputParser()

    def _get_web_context(self, query):
        try:
            results = self.tavily_tool.invoke(query)
            return "\n".join([f"- {r['content']} (Nguồn: {r['url']})" for r in results])
        except:
            return "Không có dữ liệu internet."

    def chat(self, question: str) -> str:
        print("⚡ Đang tìm kiếm thông tin...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f_internal = executor.submit(self.retriever.invoke, question)
            f_web = executor.submit(self._get_web_context, question)

            internal_docs = f_internal.result()
            web_context = f_web.result()

        internal_context = "\n".join([d.page_content for d in internal_docs])

        response = self.chain.invoke({
            "internal_context": internal_context if internal_context.strip() else "Trống",
            "web_context": web_context,
            "question": question
        })
        return response.replace("<|im_end|>", "").strip()
