from mdutils import MdUtils


class AnalysisService:
    def __init__(self):
        self.file = MdUtils(file_name='analysis', title='')

    def fill_file_with_default_content(self, standard_table_content, standard_dict):
        self.file.new_header(level=1, title='عنوان تحلیل را اینجا وارد نمایید')

        self.file.new_line('\n')
        self.file.new_header(level=2, title='خواسته‌های PO')
        self.file.new_line('لطفا توضیح کوتاهی درباره خواسته PO در این تسک وارد نمایید')

        self.file.new_line('\n\n')
        self.file.new_header(level=2, title='استاندارد نام گذاری')

        self.file.new_line()
        self.file.new_table(
            columns=2,
            rows=int(len(standard_table_content) / 2),
            text=standard_table_content,
            text_align='center'
        )

        self.file.new_line('\n')
        self.file.new_header(level=2, title='توضیح هر سطر جدول')

        for scope in standard_dict:
            self.file.new_header(level=3, title=scope)
            self.file.new_list(standard_dict[scope])
            self.file.new_line('توضیحات این بخش را اینجا وارد نمایید')
            self.file.new_line('\n\n')

        self.file.new_header(level=2, title='ابهامات')
        self.file.new_line('در صورت وجود ابهام و یا سوالی آنرا اینجا وارد نمایید')

        self.file.new_line('\n\n')
        self.file.new_header(level=2, title='دیگر توضیحات')
        self.file.new_line('هر توضیح دیگری که در قالب بالا جا نمی‌گیرد را اینجا وارد نمایید')

    def read_file(self):
        return self.file.title + self.file.table_of_contents + self.file.file_data_text + self.file.reference.get_references_as_markdown(),
