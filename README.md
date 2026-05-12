## Kiến trúc Hệ thống (System Architecture)

Dưới đây là sơ đồ luồng hoạt động tổng thể của hệ thống UIT-AI-Admissions-Copilot, từ giai đoạn tiền xử lý dữ liệu (Offline Ingestion) đến quy trình truy vấn thời gian thực (Online Query Flow):

<div align="center">
  <img src="https://github.com/user-attachments/assets/383910c9-60cc-4dc4-9e07-7a3722765620" alt="Kiến trúc ChatBot UIT" width="100%">
</div>

---

### Cấu trúc Code cốt lõi

Cấu trúc các Class được triển khai trong hệ thống, phân chia theo từng giai đoạn xử lý trên sơ đồ:

```text
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
├── 3. AI Agents & LLM Integration (Bộ脑 Chatbot)
│   └── Class AdmissionsChatbot
│       ├── __init__()
│       ├── _get_web_context()     # Bổ trợ ngữ cảnh bằng Internet (Web Search)
│       └── chat()                 # Kỹ thuật 4: Đưa Context và Query vào LLM (Qwen) sinh câu trả lời
│
└── 4. User Interface (Giao diện Gradio)
    ├── process_new_files()        # Upload tài liệu mới và cập nhật DB tự động
    └── respond()                  # Giao tiếp với người dùng

---

## Tổng kết dự án (Project Summary)

### Chức năng chính
Hệ thống là một trợ lý ảo tư vấn tuyển sinh thông minh, có khả năng ghi nhớ ngữ cảnh hội thoại để đưa ra phản hồi liên tục và phù hợp. Bên cạnh việc giải đáp chính xác dựa trên nguồn dữ liệu nội bộ chính thống, chatbot còn tích hợp khả năng tra cứu Web theo thời gian thực để cập nhật các thông tin xã hội (ví dụ: giá xăng, tin tức mới). Đặc biệt, hệ thống cho phép người dùng trực tiếp tải lên các file PDF mới để cập nhật và mở rộng kho tri thức một cách linh hoạt.

###  Cải tiến kỹ thuật (Advanced RAG)
Dự án được nâng cấp lên quy trình **Advanced RAG** với những cải tiến vượt trội so với các hệ thống truyền thống:
* **Semantic Chunking:** Thay thế cho cách cắt văn bản theo độ dài cố định, giúp bảo toàn trọn vẹn ngữ cảnh và ý nghĩa của từng đoạn thông tin.
* **Hybrid Retrieval:** Kết hợp sức mạnh của cả tìm kiếm theo ngữ nghĩa (Vector Search) và tìm kiếm theo từ khóa chính xác (BM25) để tối ưu hóa khả năng truy xuất.
* **Cross-Encoder Re-ranker:** Tích hợp bộ lọc sâu sau bước truy xuất để chấm điểm lại mức độ liên quan, đảm bảo chỉ những thông tin chuẩn xác nhất mới được đưa vào mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời, loại bỏ tối đa hiện tượng "ảo giác" (hallucination).
