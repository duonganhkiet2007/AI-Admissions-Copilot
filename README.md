## Kiến trúc Hệ thống (System Architecture)

Dưới đây là cấu trúc các Class cốt lõi được xây dựng trong hệ thống RAG, phân chia theo từng giai đoạn xử lý:

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
│       └── split()                # Cắt văn bản thông minh theo ngữ nghĩa
│
├── 2. Database & Retrieval (Lưu trữ & Truy xuất)
│   ├── Class HybridVectorDB
│   │   ├── __init__()             # Khởi tạo ChromaDB (Vector) & BM25 (Keyword)
│   │   └── get_retriever()
│   │
│   ├── Class HybridRetriever
│   │   ├── _get_relevant_documents()  # Truy xuất lai (Hybrid Search)
│   │   └── _reciprocal_rank_fusion()  # Trộn và xếp hạng kết quả (RRF)
│   │
│   └── Class CrossEncoderReranker
│       ├── __init__()
│       └── rerank()               # Chấm điểm & lọc kết quả tinh hoa (Deep Learning)
│
├── 3. AI Agents & LLM Integration (Bộ não Chatbot)
│   └── Class AdmissionsChatbot
│       ├── __init__()
│       ├── _get_web_context()     # Cào dữ liệu Internet thời gian thực
│       └── chat()                 # Multi-threading tổng hợp Nội bộ & Web
│
└── 4. User Interface (Giao diện Gradio)
    ├── process_new_files()        # Hàm tải & tự động học tài liệu mới
    └── respond()                  # Hàm xử lý luồng tin nhắn UI

Dataset
