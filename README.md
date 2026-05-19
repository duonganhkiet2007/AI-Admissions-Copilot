## Kiến trúc Hệ thống (System Architecture)

Dưới đây là sơ đồ luồng hoạt động tổng thể của hệ thống UIT-AI-Admissions-Copilot, từ giai đoạn tiền xử lý dữ liệu đến quy trình truy vấn thời gian thực:

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
│   │   ├── load_pdf()             # Đọc file PDF bằng OCR 
│   │   └── load_dir()             # Đọc toàn bộ thư mục PDF
│   │
│   └── Class SemanticChunker
│       ├── __init__()
│       ├── _split_into_sentences()
│       ├── _calculate_cosine_similarity()    # Cắt văn bản thông minh theo ngữ nghĩa
│       ├── _chunk_by_semantic_similarity()
│       └── split()                 
│
├── 2. Database & Retrieval (Lưu trữ & Truy xuất)
│   ├── Class HybridVectorDB
│   │   ├── __init__()             # Khởi tạo DB: ChromaDB (Vector) & BM25 (Keyword)
│   │   └── get_retriever()
│   │
│   ├── Class HybridRetriever
│   │   ├── _get_relevant_documents()  # Truy xuất hỗn hợp (Vector + BM25)
│   │   └── _reciprocal_rank_fusion()  # Trộn và xếp hạng kết quả bằng thuật toán RRF
│   │
│   └── Class CrossEncoderReranker
│       ├── __init__()
│       └── rerank()               # Lọc tinh và tái xếp hạng 
│
├── 3. AI Core (LLM & Web Search)
│   ├── get_llm()                  # Tải và cấu hình mô hình Qwen 1.5B Instruct bằng HuggingFacePipeline
│   └── search_web_tool            # Khởi tạo công cụ tra cứu Internet thời gian thực (Tavily Search API)
│
├── 4. LLM Integration (Chatbot)
│   └── Class AdmissionsChatbot
│       ├── __init__()
│       ├── _get_web_context()     # Bổ trợ ngữ cảnh bằng Internet (Web Search)
│       └── chat()                 # Đưa Context và Query vào LLM sinh câu trả lời
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
* **Tích hợp đa nguồn:** Bên cạnh việc giải đáp chính xác từ dữ liệu nội bộ chính thống, chatbot còn có khả năng tra cứu Web theo thời gian thực (ví dụ: giá xăng, tin tức mới) để bổ sung thông tin, cho người dùng upload thêm dữ liệu.
* **Cập nhật tri thức động:** Cho phép người dùng trực tiếp tải lên các file PDF mới để mở rộng và cập nhật kho dữ liệu một cách linh hoạt.

### Cải tiến kỹ thuật (Advanced RAG)

Dự án được nâng cấp lên quy trình Advanced RAG với những cải tiến vượt trội so với các hệ thống truyền thống:

* **Semantic Chunking:**
   Khắc phục nhược điểm của phương pháp cắt văn bản theo độ dài cố định (fixed-size chunking) truyền thống. Kỹ thuật này sử dụng mô hình embedding để đánh giá độ tương đồng ngữ nghĩa giữa các câu liền kề, từ đó tự động xác định ranh giới và nhóm các nội dung cùng chủ đề lại với nhau.

   Việc này giúp bảo toàn trọn vẹn ngữ cảnh, tránh tình trạng một ý tưởng bị cắt xén giữa chừng, đảm bảo LLM luôn nhận được luồng thông tin đầu vào đầy đủ và chuẩn xác nhất.

---
  <div align="center">
  <img width="100%" alt="Mô tả ảnh của bạn ở đây" src="https://github.com/user-attachments/assets/6c2c80c6-5bd7-4ac1-be13-b765c5349ff5" />
</div>

---
* **Hybrid Retrieval:**
  Là sự kết hợp hoàn hảo giữa tìm kiếm ngữ nghĩa (Vector Search) và tìm kiếm từ khóa (BM25). Phương pháp này khắc phục triệt để nhược điểm thiếu chính xác với từ khóa đặc thù/viết tắt của Vector Search và kém hiểu ngữ cảnh của BM25.
  
  Kết quả từ hai luồng sau đó được trộn và tối ưu hóa bằng thuật toán Reciprocal Rank Fusion (RRF), đảm bảo tài liệu trả về vừa đúng ý định người dùng, vừa chuẩn xác từng thuật ngữ chuyên ngành.
---

<img width="1200" height="655" alt="image" src="https://github.com/user-attachments/assets/373a374c-61c5-41e3-b667-d850eec81656" />

---
* **Cross-Encoder Re-ranker:**
  Thay vì chỉ đánh giá vector độc lập, mô hình Cross-Encoder sẽ ghép cặp trực tiếp "Câu hỏi" và "Tài liệu" để phân tích sự chú ý (cross-attention) giữa chúng.

  Quá trình này giúp tái xếp hạng (re-rank) toàn bộ kết quả, loại bỏ triệt để các thông tin nhiễu có thể lọt qua ở bước truy xuất ban đầu, đảm bảo LLM chỉ nhận được những ngữ cảnh thực sự chất lượng.
---

<img width="1400" height="411" alt="image" src="https://github.com/user-attachments/assets/37ee7ab5-b965-42d6-947f-38c064360146" />

---
