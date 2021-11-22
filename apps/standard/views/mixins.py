from copy import deepcopy

from django.http import HttpResponse

from ..services import MarkdownService


class AnalysisFileGeneratorMixin:
    def _get_clean_POST_data(self, request):
        data = deepcopy(request.POST)
        del data['csrfmiddlewaretoken']
        return data

    @staticmethod
    def _generate_md_file(standard_table_content, standard_dict):
        md_service = MarkdownService(file_name='analysis')
        md_service.file.new_header(level=1, title='عنوان تحلیل را اینجا وارد نمایید')

        md_service.file.new_line('\n')
        md_service.file.new_header(level=2, title='استاندارد نام گذاری')

        md_service.file.new_line()
        md_service.file.new_table(
            columns=2,
            rows=int(len(standard_table_content) / 2),
            text=standard_table_content,
            text_align='center'
        )

        md_service.file.new_line('\n')
        md_service.file.new_header(level=2, title='توضیح هر سطر جدول')

        for scope in standard_dict:
            md_service.file.new_header(level=3, title=scope)
            md_service.file.new_list(standard_dict[scope])
            md_service.file.new_line('توضیحات این بخش را اینجا وارد نمایید')
            md_service.file.new_line('\n\n')

        md_service.file.new_header(level=2, title='ابهامات')
        md_service.file.new_line('در صورت وجود ابهام و یا سوالی آنرا اینجا وارد نمایید')

        md_service.file.new_line('\n\n')
        md_service.file.new_header(level=2, title='دیگر توضیحات')
        md_service.file.new_line('هر توضیح دیگری که در قالب بالا جا نمی‌گیرد را اینجا وارد نمایید')

        return md_service

    def post(self, request):
        standard_table_content = ['فایل/مفهوم', 'مقدار']
        standard_dict = {}
        for scope in self._get_clean_POST_data(request):
            for value in request.POST.getlist(scope):
                standard_table_content.extend([scope, value])
                standard_dict.setdefault(scope, []).append(value)

        md_service = self._generate_md_file(standard_table_content, standard_dict)

        response = HttpResponse(
            md_service.read_file(),
            content_type='text/markdown',
            headers={'Content-Disposition': f'attachment; filename="analysis_{request.GET["entity"]}.md"'},
        )
        return response
