import xlwt, xlrd, os
import datetime
import mimetypes
from django.conf import settings
from django.http import FileResponse


class ExcelFileHandler(object):
    '''
    Excel文件生成和下载
    '''

    def __init__(self, header):
        self.header = header
        self.ws = None
        self.wb = None

    def create_style(self):
        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
        return style0

    def create_wb(self):
        wb = xlwt.Workbook()
        self.wb = wb

    def create_sheet(self):
        self.create_wb()
        self.ws = self.wb.add_sheet('Sheet', cell_overwrite_ok=True)

    def create_header(self):
        '''
        创建表头
        :return:
        '''

        style0 = self.create_style()
        self.create_sheet()
        for i in range(len(self.header)):
            self.ws.write(0, i, self.header[i], style0)

    def write_row_data(self, data_list):
        '''
        写入每一行数据
        :param data_list:
        :return:
        '''
        self.create_header()
        if isinstance(data_list, list):
            for i in range(len(data_list)):
                for j in range(len(data_list[i])):
                    self.ws.write(i + 1, j, data_list[i][j])

    def save_file(self, data_list):
        '''
        保存文件
        :param data_list:
        :return:
        '''
        self.write_row_data(data_list)
        timestr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = 'New-' + timestr + '.xls'
        file_path = os.path.join(settings.BASE_DIR, 'Django_apps', 'web', 'files', file_name)
        self.wb.save(file_path)
        return file_path

    def down_load_file(self, data_list):
        '''
        下载生成的excel文件
        :param data_list:
        :return:
        '''
        file_path = self.save_file(data_list)
        fp = open(file_path, 'rb')
        content_type = mimetypes.guess_type(file_path)[0]
        response = FileResponse(fp, content_type=content_type)
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path)
        return response, file_path

    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)


class ExcelUploadHandler(object):
    def __init__(self, file):
        self.file = file

    def open_excel(self):
        workbook = xlrd.open_workbook(file_contents=self.file.file.read())
        return workbook

    def trans_datetime(self, cell):
        time = datetime.datetime(*xlrd.xldate_as_tuple(cell, 0))
        return time