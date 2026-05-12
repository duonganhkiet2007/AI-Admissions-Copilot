## Kiến trúc Hệ thống (System Architecture)

Dưới đây là sơ đồ luồng hoạt động tổng thể của hệ thống UIT-AI-Admissions-Copilot, từ giai đoạn tiền xử lý dữ liệu (Offline Ingestion) đến quy trình truy vấn thời gian thực (Online Query Flow):

<div align="center">
  <img src="https://github.com/user-attachments/assets/383910c9-60cc-4dc4-9e07-7a3722765620" alt="Kiến trúc ChatBot UIT" width="100%">
</div>

---

### Cấu trúc Code cốt lõi

Cấu trúc các Class được triển khai trong hệ thống, phân chia theo từng giai đoạn xử lý trên sơ đồ:
```
UIT-AI-Admissions-Copilot
├── 1. Data Ingestion & Processing (Xử lý Dữ liệu)
│   ├── Class SimpleLoader
│   │   ├── load_pdf()             # Đọc file PDF bằng OCR (Tesseract)
│   │   └── load_dir()             # Đọc toàn bộ thư mục PDF
│   │
│   └── Class SemanticChunker
│       ├── __init__()
│       ├── _split_into_sentences()
│       ├── _calculate_cosine_similarity()
│       ├── _chunk_by_semantic_similarity()
│       └── split()                # Cắt văn bản thông minh theo ngữ nghĩa (Kỹ thuật 1)
│
├── 2. Database & Retrieval (Lưu trữ & Truy xuất)
│   ├── Class HybridVectorDB
│   │   ├── __init__()             # Khởi tạo DB Lai: ChromaDB (Vector) & BM25 (Keyword)
│   │   └── get_retriever()
│   │
│   ├── Class HybridRetriever
│   │   ├── _get_relevant_documents()  # Kỹ thuật 2: Truy xuất hỗn hợp (Vector + BM25)
│   │   └── _reciprocal_rank_fusion()  # Trộn và xếp hạng kết quả bằng thuật toán RRF
│   │
│   └── Class CrossEncoderReranker
│       ├── __init__()
│       └── rerank()               # Kỹ thuật 3: Lọc tinh và tái xếp hạng bằng Deep Learning
│
├── 3. AI Core (LLM & Web Search)
│   ├── get_llm()                  # Tải và cấu hình mô hình Qwen 1.5B Instruct bằng HuggingFacePipeline
│   └── search_web_tool            # Khởi tạo công cụ tra cứu Internet thời gian thực (Tavily Search API)
│
├── 4. LLM Integration (Chatbot)
│   └── Class AdmissionsChatbot
│       ├── __init__()
│       ├── _get_web_context()     # Bổ trợ ngữ cảnh bằng Internet (Web Search)
│       └── chat()                 # Kỹ thuật 4: Đưa Context và Query vào LLM sinh câu trả lời
│
└── 5. User Interface (Giao diện Gradio)
    ├── process_new_files()        # Upload tài liệu mới và cập nhật DB tự động
    └── respond()                  # Giao tiếp với người dùng
```
## Giao diện ChatBot 

<div align="center">
  <img width="1918" height="873" alt="image" src="https://github.com/user-attachments/assets/ab52ab64-80ae-4ad8-ae42-8ce32b336aca" />
</div>


---

## Tổng kết dự án (Project Summary)

### Chức năng chính

* **Trợ lý ảo thông minh:** Hệ thống có khả năng ghi nhớ ngữ cảnh hội thoại để đưa ra phản hồi liên tục và phù hợp với nội dung trước đó.
* **Tích hợp đa nguồn:** Bên cạnh việc giải đáp chính xác từ dữ liệu nội bộ chính thống, chatbot còn có khả năng tra cứu Web theo thời gian thực (ví dụ: giá xăng, tin tức mới) để bổ sung thông tin.
* **Cập nhật tri thức động:** Cho phép người dùng trực tiếp tải lên các file PDF mới để mở rộng và cập nhật kho dữ liệu một cách linh hoạt.

### Cải tiến kỹ thuật (Advanced RAG)

Dự án được nâng cấp lên quy trình Advanced RAG với những cải tiến vượt trội so với các hệ thống truyền thống:

* **Semantic Chunking:** Thay thế cho cách cắt văn bản theo độ dài cố định, giúp bảo toàn trọn vẹn ngữ cảnh và ý nghĩa của từng đoạn thông tin.
* **Hybrid Retrieval:** Kết hợp sức mạnh của cả tìm kiếm theo ngữ nghĩa (Vector Search) và tìm kiếm theo từ khóa chính xác (BM25) để tối ưu hóa khả năng truy xuất.
* **Cross-Encoder Re-ranker:** Nó tự động chấm điểm độ liên quan trực tiếp giữa câu hỏi và tài liệu, qua đó loại bỏ thông tin nhiễu.
