# 导入所需的模块
from edge_pdf import PDFProcessor, DataFrameTransformer, DataFrameDirectoryTree
import sys

if __name__ == '__main__':
    # 设置PDF文件路径和保存路径
    p_pdf_path = "./src/modified_pdf_file.pdf"
    p_save_path = "./src/data.pdf"

    # 使用PDFProcessor处理PDF文件并获取原始数据
    processor = PDFProcessor(p_pdf_path)
    origin_data = processor.return_df

    # 如果原始数据为空，则退出程序
    if origin_data.empty:
        sys.exit(0)

    # 创建DataFrameDirectoryTree对象，并根据指定列构建目录树
    tree = DataFrameDirectoryTree(origin_data, "content")
    origin_data["reply"] = origin_data["id"].apply(tree.get_subdirectories)

    # 重新排列列的顺序
    origin_data = origin_data.reindex(
        columns=["Page", "content", "reply", "id", "parent_id", "creationDate", "modDate",
                 "vertices", "subject", "title"])

    # 使用DataFrameTransformer对origin_data进行转换
    df_b = DataFrameTransformer(origin_data, "reply").transform

    # 仅保留parent_id为空的行
    df_b = df_b[df_b["parent_id"].isnull()]

    # 复制df_b并删除"index"列
    df_c = df_b.reset_index().copy()
    df_c.drop(["index"], axis=1, inplace=True)

    # 将df_c保存为Excel文件
    df_c.to_excel(p_save_path, "目录")


    #
    # file_path = './src/d28c83cb2ca5bd0e9bf4ece29f52bdff(1).pdf'
    # output_path = './src/modified_pdf_file.pdf'
    # search_text = '员工'
    #
    # pdf_editor = PDFEditor(file_path)
    # pdf_editor.search_and_highlight(search_text)
    #
    # for page_number in range(pdf_editor.pdf.page_count):
    #     page = pdf_editor.pdf[page_number]
    #     search_results = page.search_for(search_text)
    #     for rect in search_results:
    #         rect = (page_number, rect.x0, rect.y0 - 20, rect.x1 + 100, rect.y0)
    #         content_text = search_text
    #         pdf_editor.add_text_annotation(page_number, rect, content_text)
    #
    # pdf_editor.save(output_path)
