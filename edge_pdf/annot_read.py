import fitz
import pandas as pd
import datetime
import argparse


class PDFProcessor:

    def __init__(self, cls_pdf_path):
        self.doc = None
        self.pdf_path = cls_pdf_path
        self.sheet_col = ["Page", "content", "id", "parent_id", "creationDate", "modDate", "subject", "title",
                          "vertices"]
        self.df = pd.DataFrame(columns=self.sheet_col)
        self.process_pdf()

    @classmethod
    def parse_datetime(cls, ins_date_str):
        date_str = ins_date_str.replace('D:', '')

        # 解析日期时间字符串
        date_format = "%Y%m%d%H%M%S"
        datetime_obj = datetime.datetime.strptime(date_str[:14], date_format)

        # 创建 pandas 的 Timestamp 对象
        timestamp_obj = pd.Timestamp(datetime_obj)

        return timestamp_obj

    def process_pdf(self):
        self.doc = fitz.open(self.pdf_path)
        for page_num, page in enumerate(self.doc, start=1):
            annotations = page.annots()
            if annotations:
                for annot in annotations:

                    if annot.info['subject'] != "":
                        page_info = [int(page_num), annot.info["content"], int(annot.xref), int(annot.irt_xref),
                                     self.parse_datetime(annot.info["creationDate"]),
                                     self.parse_datetime(annot.info['modDate']),
                                     annot.info['subject'], annot.info['title'], annot.vertices]
                        # page_info = [page_num, annot.info["content"], annot.popup_xref,annot.irt_xref, annot.xref]
                        newpdf = pd.DataFrame([page_info], columns=self.df.columns)
                        self.df = pd.concat([self.df, newpdf], ignore_index=True)
        self.doc.close()

    @property
    def return_df(self):
        self.df = self.df.reset_index(drop=True)
        self.df["parent_id"] = self.df["parent_id"].replace(0, None)
        return self.df


class DataFrameDirectoryTree:

    def __init__(self, cls_data, cls_name=None, cls_id=None, cls_parent_id=None):
        # self.get_sub_id = None
        self.name = cls_name
        self.id = cls_id
        self.parent_id = cls_parent_id
        if cls_name is None:
            self.name = 'name'
        if cls_id is None:
            self.id = 'id'
        if cls_parent_id is None:
            self.parent_id = 'parent_id'
        self.df = pd.DataFrame(cls_data)

    def get_subdirectories(self, parent_id):
        result = []
        for index, row in self.df.iterrows():
            if row[self.parent_id] == parent_id:
                result.append(row[self.name])
                result.extend(self.get_subdirectories(row[self.id]))
        return result

    def get_sub_id(self, parent_id):
        result = []
        for index, row in self.df.iterrows():
            if row[self.parent_id] == parent_id:
                result.append(row[self.id])
                result.extend(self.get_sub_id(row[self.id]))
        return result

    def get_parent_id(self, ins_id):
        result = []
        for index, row in self.df.iterrows():
            if row[self.id] == ins_id:
                result.append(row[self.parent_id])
                result.extend(self.get_parent_id(row[self.parent_id]))
        return result

    def get_parent_name(self, ins_id):
        result = []
        for index, row in self.df.iterrows():
            if row[self.id] == ins_id:
                result.append(row[self.name])
                result.extend(self.get_parent_name(row[self.parent_id]))
        return result


class DataFrameTransformer:

    def __init__(self, cls_data, cls_name=None):
        self.name = cls_name
        if cls_name is None:
            self.name = 'path_name'
        self.data = cls_data
        self.df_A = pd.DataFrame(self.data)

    @property
    def transform(self):
        max_length = self.df_A[self.name].apply(len).max()

        for i in range(max_length):
            self.df_A[self.name + str(i + 1)] = self.df_A[self.name].apply(lambda x: x[i] if len(x) > i else '')

        return self.df_A


def main(p_pdf_path=None, p_save_path=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', default="../src/modified_pdf_file.pdf", help='请指定输入pdf文件路径')
    parser.add_argument('--out', default="../src/data.xlsx", help='请指定输出xlsx文件')
    args = parser.parse_args()
    if p_pdf_path is None:
        p_pdf_path = args.pdf
    if p_save_path is None:
        p_save_path = args.out
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


# 创建PDFProcessor对象
if __name__ == "__main__":
    main()
