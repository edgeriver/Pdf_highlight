# dege_pdf Pdf的注释工具

PDFMiner is a text extraction tool for PDF documents.

## 构建
    python setup.py sdist bdist_wheel
    twine upload dist/*

## 安装命令
ssh安装

    pip install git+ssh://git@github.com/edgeriver/Pdf_highlight.git

https安装

    pip instal git+https://github.com/edgeriver/Pdf_highlight.git


## 命令行语法
    annot_export --pdf=file.pdf --out=data.xlsx

## 包的使用方法
    # 导出注释的用户
    from edge_pdf import annot_export
    
    if __name__ == '__main__':
        # 获取注释文件
        p_pdf_path = "src/need_annot.pdf"
        p_save_path = "src/data2.xlsx"
        annot_export(p_pdf_path,p_save_path)
