import fitz
import argparse


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


def main(file_path=None, output_path=None, search_text=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default="../src/sample.pdf", help='请指定输入pdf文件路径')
    parser.add_argument('--out', default="../src/data.pdf", help='请指定输出pdf文件路径')
    parser.add_argument('--search', default="员工", help='搜索的关键词')
    args = parser.parse_args()

    file_path = file_path or args.file
    output_path = output_path or args.out
    search_text = search_text or args.search

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


if __name__ == '__main__':
    main()
