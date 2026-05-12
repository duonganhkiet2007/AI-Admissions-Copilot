class SimpleLoader:
    def load_pdf(self, pdf_file: str) -> List[Document]:
        processed_docs = []
        try:
            # Convert all pages to images
            images = convert_from_path(pdf_file, dpi=300)
            total_pages = len(images)

            for i in tqdm(range(total_pages), desc=f"Performing OCR on {os.path.basename(pdf_file)}"):
                current_image = images[i]
                try:
                    ocr_text = pytesseract.image_to_string(current_image, lang='vie') # 'vie' for Vietnamese

                    # Inlined cleaning logic
                    cleaned_content = unicodedata.normalize("NFC", ocr_text)
                    cleaned_content = re.sub(r"\s+", " ", cleaned_content) # Replace multiple whitespace with single space
                    cleaned_content = re.sub(r"\n\s*\n", "\n", cleaned_content) # Replace multiple newlines with single newline
                    cleaned_content = cleaned_content.strip()

                    if cleaned_content:
                        doc = Document(page_content=cleaned_content, metadata={
                            "source": pdf_file,
                            "page": i, # 0-indexed page number
                            "page_label": str(i + 1) # 1-indexed page label
                        })
                        processed_docs.append(doc)
                    else:
                        print(f" OCR extracted no usable text for page {i+1} from {os.path.basename(pdf_file)}.")
                except Exception as e:
                    print(f" OCR failed for page {i+1} of {os.path.basename(pdf_file)} with error: {e}")

        except Exception as e:
            print(f"Error loading PDF or performing OCR on {os.path.basename(pdf_file)}: {e}")
            return []

        return processed_docs

    def load_dir(self, dir_path: str) -> List[Document]:
        pdf_files = glob.glob(f"{dir_path}/*.pdf")
        if not pdf_files:
            print(f" Không tìm thấy file PDF nào trong {dir_path}.")
            return []

        all_docs = []
        for pdf_file in tqdm(pdf_files, desc="Đang đọc PDFs"):
            all_docs.extend(self.load_pdf(pdf_file))
        return all_docs
