from edge_pdf import PDFEditor

if __name__ == '__main__':

    file_path = './src/d28c83cb2ca5bd0e9bf4ece29f52bdff(1).pdf'
    output_path = './src/modified_pdf_file.pdf'
    search_text = '员工'

    pdf_editor = PDFEditor(file_path)
    pdf_editor.search_and_highlight(search_text)

    for page_number in range(pdf_editor.pdf.page_count):
        page = pdf_editor.pdf[page_number]
        search_results = page.search_for(search_text)
        for rect in search_results:
            rect = (page_number, rect.x0, rect.y0 - 20, rect.x1 + 100, rect.y0)
            content_text = search_text
            pdf_editor.add_text_annotation(page_number, rect, content_text)

    pdf_editor.save(output_path)