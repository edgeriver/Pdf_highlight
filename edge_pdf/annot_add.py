import fitz


class PDFEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf = fitz.open(file_path)

    def search_and_highlight(self, search_text):
        for page_number in range(self.pdf.page_count):
            page = self.pdf[page_number]
            search_results = page.search_for(search_text)
            for rect in search_results:
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(stroke=(0, 1, 0))
                highlight.set_opacity(0.5)
                highlight.update()

    def add_text_annotation(self, page_number, rect, content_text):
        page = self.pdf[page_number]
        content_rect = fitz.Rect(rect[1], rect[2], rect[3], rect[4])
        content_annot = page.add_text_annot(content_rect, content_text)
        content_annot.set_colors(fill=(1, 1, 0))
        content_annot.update()

    def save(self, output_path):
        self.pdf.save(output_path)
        self.pdf.close()


if __name__ == '__main__':

    file_path = '../src/d28c83cb2ca5bd0e9bf4ece29f52bdff(1).pdf'
    output_path = '../src/modified_pdf_file.pdf'
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
