try:
    if 'retriever' in globals() and 'llm' in globals():
        rag_bot = AdmissionsChatbot(
            llm=llm,
            retriever=retriever,
            internal_vdb=hybrid_vector_db.vector_db,
            embeddings=embeddings
        )
        print("✅ Rag bot đã được khởi tạo mặc định.")
    else:
        rag_bot = None
except Exception as e:
    print(f"Lỗi khởi tạo mặc định: {e}")
    rag_bot = None

# Updated CSS for a more compact, top-aligned layout
custom_css = """
body, .gradio-container {
    background-color: #f0f7ff !important;
}
.gradio-container {
    margin-top: 5px !important;
    padding-top: 0px !important;
}
.white-card {
    background-color: #ffffff !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.08) !important;
    padding: 15px !important;
    margin: 5px !important;
}
.gradio-dataset {
    background-color: #eff6ff;
    border: 1px dashed #bfdbfe !important;
}
.gradio-chat, .gradio-textbox {
    border: none !important;
    box-shadow: none !important;
}
.gradio-message.bot {
    background-color: #f0f9ff !important;
}
.header-content {
    text-align: center;
    margin-bottom: 10px !important;
    display: flex;
    justify-content: center;
}
.title-box {
    background-color: #ffffff !important;
    border: 2px solid #1e40af;
    border-radius: 50px !important;
    padding: 10px 40px !important;
    display: inline-block;
    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15) !important;
}
.header-title {
    font-size: 2em;
    font-weight: 800;
    color: #1e40af;
    margin: 0 !important;
}

.update-btn-style {
    background: #1e3a8a !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
.submit-btn-style {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
"""

def process_new_files(file_list):
    if not file_list:
        return "⚠️ Vui lòng tải lên ít nhất một file."
    try:
        all_new_docs = []
        for file_obj in file_list:
            new_docs = loader.load_pdf(file_obj.name)
            all_new_docs.extend(new_docs)
        if not all_new_docs:
            return "❌ Không thể trích xuất văn bản từ các file đã chọn."
        new_chunks = semantic_chunker.split(all_new_docs)
        global hybrid_vector_db, retriever, rag_bot
        hybrid_vector_db = HybridVectorDB(documents=new_chunks, embedding=embeddings)
        retriever = hybrid_vector_db.get_retriever(search_kwargs={"k": 5})

        rag_bot = AdmissionsChatbot(
            llm=llm,
            retriever=retriever,
            internal_vdb=hybrid_vector_db.vector_db,
            embeddings=embeddings
        )
        return f"✅ Đã cập nhật thành công {len(new_chunks)} phân đoạn."
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"

def respond(message, history):
    global rag_bot
    if not message or not message.strip():
        return "", history

    if 'rag_bot' not in globals() or rag_bot is None:
        bot_response = "⚠️ Hệ thống chưa sẵn sàng. Vui lòng nhấn 'Cập nhật hệ thống' để khởi tạo dữ liệu."
    else:
        try:
            bot_response = rag_bot.chat(message)
        except Exception as e:
            print(f"Chat Error: {traceback.format_exc()}")
            bot_response = f"❌ Đã xảy ra lỗi khi xử lý câu hỏi: {str(e)}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_response})
    return "", history

with gr.Blocks(css=custom_css) as demo:
    with gr.Row(elem_classes="header-content"):
        gr.HTML("<div class='title-box'><span class='header-title'>Chat Box tư vấn tuyển sinh UIT</span></div>")

    with gr.Row():
        with gr.Column(scale=1, elem_classes="white-card"):
            gr.Markdown("### 📁 Tài liệu")
            file_input = gr.File(label="Tải lên tài liệu mới", file_count="multiple", elem_classes="gradio-dataset")
            status_output = gr.Markdown(" *Trạng thái: Sẵn sàng* ")
            update_btn = gr.Button("🚀 Cập nhật hệ thống", elem_classes="update-btn-style")
            gr.Markdown("""
            - **Bước 1:** Tải tệp PDF lên
            - **Bước 2:** Nhấn Cập nhật
            - **Bước 3:** Bắt đầu đặt câu hỏi
            """)

        with gr.Column(scale=3, elem_classes="white-card"):
            chatbot_component = gr.Chatbot(
                type="messages",
                elem_id="chatbot",
                avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"),
                show_label=False,
                render_markdown=True,
                allow_tags=False
            )
            with gr.Row():
                msg = gr.Textbox(
                    show_label=False,
                    placeholder="Hỏi về tuyển sinh, điểm chuẩn, mã ngành...",
                    scale=7,
                    container=False
                )
                submit_btn = gr.Button("Gửi", elem_classes="submit-btn-style", scale=2)
                clear_btn = gr.Button("🗑️", scale=1)

            update_btn.click(process_new_files, inputs=[file_input], outputs=[status_output])
            msg.submit(respond, [msg, chatbot_component], [msg, chatbot_component])
            submit_btn.click(respond, [msg, chatbot_component], [msg, chatbot_component])
            clear_btn.click(lambda: [], None, chatbot_component)

demo.launch(share=True)
