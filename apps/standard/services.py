from mdutils import MdUtils


class MarkdownService:
    def __init__(self, file_name, title=''):
        self.file = MdUtils(file_name=file_name, title='')

        if title:
            self.file.new_header(level=1, title=title)

    def read_file(self):
        return self.file.title + self.file.table_of_contents + self.file.file_data_text + self.file.reference.get_references_as_markdown(),
