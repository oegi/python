import csv
from collections import defaultdict

from pyexcelerate import (
    Workbook,
    Style,
    Font,
    Alignment,
    Color)

from appcore.helpers.exceptions import ErrorException


class RegisterHelper(object):
    __slots__ = ['head', 'detail', 'detail_cn', 'channels', 'channel_quantity', 'hr_or_min', 'color_border',
                 'sheet_name']

    def __init__(self, head=None, detail=None, detail_cn=3000, channels=None, hr_or_min='1HR',
                 sheet_name='Sheet Name', ):

        if channels is None:
            channels = []

        if detail is None:
            detail = []

        if head is None:
            head = []

        self.head = head
        self.detail = detail
        self.detail_cn = detail_cn
        self.channels = channels
        self.channel_quantity = len(channels)
        self.hr_or_min = hr_or_min
        self.sheet_name = sheet_name
        self.color_border = Color(67, 71, 75)

    def save(self, output='/tmp/output.xlsx'):
        wb = Workbook()
        ws = wb.new_sheet(self.sheet_name, data=[], force_name=True)
        # head fijo, primera parte
        # corrimiento a la derecha

        factor = 6
        if self.hr_or_min == '15MIN':
            factor = 7

        ws.set_cell_value(4, factor, 'Punto de medida')
        ws.set_cell_value(5, factor, 'Coordinado')
        ws.set_cell_value(6, factor, 'Serie Medidor')
        ws.set_cell_value(7, factor, 'Subestación')
        ws.set_cell_value(8, factor, 'Fecha Ultima Lectura')
        ws.set_cell_value(9, factor, 'Principal/Respaldo')
        ws.set_cell_value(10, factor, 'ID Bitacora/F-Inicio_F-fin')

        # los titulos van a la izquierda
        ws.set_cell_style(4, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(5, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(6, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(7, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(8, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(9, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))
        ws.set_cell_style(10, factor, Style(alignment=Alignment(vertical='center', horizontal='left')))

        ws.get_cell_style(4, factor).borders.right.color = self.color_border
        ws.get_cell_style(5, factor).borders.right.color = self.color_border
        ws.get_cell_style(6, factor).borders.right.color = self.color_border
        ws.get_cell_style(7, factor).borders.right.color = self.color_border
        ws.get_cell_style(8, factor).borders.right.color = self.color_border
        ws.get_cell_style(9, factor).borders.right.color = self.color_border
        ws.get_cell_style(10, factor).borders.right.color = self.color_border

        # titulo para las fechas
        ws.set_cell_value(11, 1, 'TOTAL MENSUAL')
        style = Style(font=Font(bold=True), alignment=Alignment(vertical='center', horizontal='center'))
        ws.set_cell_style(11, 1, style)
        ws.range((11, 1), (11, factor)).merge()

        ws.set_cell_value(12, 1, 'AÑO')
        ws.set_cell_value(12, 2, 'MES')
        ws.set_cell_value(12, 3, 'DIA')
        ws.set_cell_value(12, 4, 'HORA UTC')
        ws.set_cell_value(12, 5, (self.hr_or_min == '15MIN') and 'HORA' or 'INICIO INTERVALO')

        if self.hr_or_min == '1H':
            ws.set_cell_value(12, 6, 'FIN INTERVALO')

        if self.hr_or_min == '15MIN':
            ws.set_cell_value(12, 6, 'INICIO INTERVALO')
            ws.set_cell_value(12, 7, 'FIN INTERVALO')

        # bold para anno, mes ,dia, hora, hora utc, intervalo
        style = Style(size=-1, font=Font(bold=True), alignment=Alignment(vertical='center', horizontal='center'))

        ws.set_cell_style(12, 1, style)
        ws.set_cell_style(12, 2, style)
        ws.set_cell_style(12, 3, style)
        ws.set_cell_style(12, 4, style)
        ws.set_cell_style(12, 5, style)
        ws.set_cell_style(12, 6, style)

        if self.hr_or_min == '15MIN':
            ws.set_cell_style(12, 7, style)

        ws.set_col_style(1, Style(alignment=Alignment(vertical='center', horizontal='center')))
        ws.set_col_style(2, Style(alignment=Alignment(vertical='center', horizontal='center')))
        ws.set_col_style(3, Style(alignment=Alignment(vertical='center', horizontal='center')))
        ws.set_col_style(4, Style(alignment=Alignment(vertical='center', horizontal='center')))
        ws.set_col_style(5, Style(size=20, ))
        ws.set_col_style(6, Style(size=20, ))

        if self.hr_or_min == '15MIN':
            ws.set_col_style(7, Style(size=-1, alignment=Alignment(vertical='center', horizontal='center')))

        # tamanno para la primera columna
        ws.set_col_style(1, Style(size=-1, ))
        head_i = 0
        for m in self.head:
            column_main = 7
            if self.hr_or_min == '15MIN':
                column_main = 8

            factor2 = column_main + int(head_i * self.channel_quantity)
            ws.set_cell_value(4, factor2, m.get('idsocket'))
            ws.set_cell_value(5, factor2, m.get('idclient'))
            ws.set_cell_value(6, factor2, m.get('noins'))
            ws.set_cell_value(7, factor2, m.get('user_defined01'))
            date_last_reading = m.get('date_last_reading')
            if date_last_reading is not None:
                date_last_reading = date_last_reading.__format__('%d-%m-%Y %H:%M:%S')
            ws.set_cell_value(8, factor2, date_last_reading)

            ws.set_cell_value(9, factor2, m.get('backup_des'))
            ws.set_cell_value(10, factor2, m.get('binnacles_des'))

            # BORDERS
            merge_column = (factor2 + self.channel_quantity) - 1
            ws.range((4, factor2), (4, merge_column)).style.borders.right.color = self.color_border
            ws.range((4, factor2), (4, merge_column)).merge()
            ws.range((5, factor2), (5, merge_column)).style.borders.right.color = self.color_border
            ws.range((5, factor2), (5, merge_column)).merge()
            ws.range((6, factor2), (6, merge_column)).style.borders.right.color = self.color_border
            ws.range((6, factor2), (6, merge_column)).merge()
            ws.range((7, factor2), (7, merge_column)).style.borders.right.color = self.color_border
            ws.range((7, factor2), (7, merge_column)).merge()
            ws.range((8, factor2), (8, merge_column)).style.borders.right.color = self.color_border
            ws.range((8, factor2), (8, merge_column)).merge()
            ws.range((9, factor2), (9, merge_column)).style.borders.right.color = self.color_border
            ws.range((9, factor2), (9, merge_column)).merge()
            ws.range((10, factor2), (10, merge_column)).style.borders.right.color = self.color_border
            ws.range((10, factor2), (10, merge_column)).merge()

            style = Style(
                font=Font(bold=True),
                alignment=Alignment(vertical='center', horizontal='center'),
            )

            ws.set_cell_style(4, factor2, style)
            ws.set_cell_style(5, factor2, style)
            ws.set_cell_style(6, factor2, style)
            ws.set_cell_style(7, factor2, style)
            ws.set_cell_style(8, factor2, style)
            ws.set_cell_style(9, factor2, style)
            ws.set_cell_style(10, factor2, style)

            channel_i = 0
            user_defined59 = m.get('user_defined59')
            for channel in self.channels:
                chn_i = factor2 + channel_i

                # HEAD HORIZONTAL - CALCULATE SUM
                letter = self.__get_letter(chn_i)
                range_background = '{}9'.format(letter)
                ws.range(range_background, range_background).style.fill.background = Color(143, 180, 236, 0)

                chn_c = '=SUM({}{}:{}3000)'.format(letter, 13, letter)
                ws.set_cell_value(11, chn_i, chn_c)
                ws.get_cell_style(11, chn_i).format.format = '#,##0.00'

                # HEAD HORIZONTAL - STYLES
                ws.set_col_style(chn_i, Style(alignment=Alignment(vertical='center', horizontal='center')))

                if channel_i == (self.channel_quantity - 1):
                    ws.get_cell_style(11, chn_i).borders.right.color = self.color_border

                description = (user_defined59 == '1') and channel.get('description1') or channel.get('description2')
                # HEAD HORIZONTAL
                ws.set_cell_value(12, chn_i, '{}'.format(description))
                if channel_i == (self.channel_quantity - 1):
                    ws.get_cell_style(12, chn_i).borders.right.color = self.color_border

                ws.set_col_style(chn_i, Style(size=-1))

                channel_i = channel_i + 1
            head_i += 1

        # continuuar
        ws.range((11, 1), (self.detail_cn + 12, 1)).style.fill.background = Color(143, 180, 236, 0)
        ws.range((13, 2), (self.detail_cn + 12, 2)).style.fill.background = Color(198, 217, 248, 0)
        ws.range((13, 3), (self.detail_cn + 12, 3)).style.fill.background = Color(198, 217, 248, 0)
        ws.range((13, 4), (self.detail_cn + 12, 4)).style.fill.background = Color(198, 217, 248, 0)
        ws.range((13, 5), (self.detail_cn + 12, 5)).style.fill.background = Color(198, 217, 248, 0)
        ws.range((13, 6), (self.detail_cn + 12, 6)).style.fill.background = Color(198, 217, 248, 0)
        if self.hr_or_min == '15MIN':
            ws.range((13, 7), (self.detail_cn + 12, 7)).style.fill.background = Color(198, 217, 248, 0)
        ws.range((11, 1), (self.detail_cn + 12, 1)).style.alignment = Alignment(vertical='center', horizontal='center')

        counter = 1
        channel_value = 7
        if self.hr_or_min == '15MIN':
            channel_value = 8

        # CREATE VARIABLE DYNAMIC
        while self.channel_quantity >= counter:
            globals()['channel_q_{}'.format(counter, )] = channel_value
            channel_value += 1
            counter += 1

        # DETAIL (MEASURE_DETAIL)
        for _i, _d in enumerate(self.detail):
            print("->")
            for _j in self.detail[_d]:
                row = 13
                for k, data in enumerate(self.detail[_d][_j]):
                    yearx = data.get('yearx')
                    monthx = data.get('monthx')
                    dayx = data.get('dayx')
                    hourx = data.get('hourx')
                    utchourx = data.get('utchourx')

                    if _i == 0:
                        ws.set_cell_value(row, 1, yearx)
                        ws.set_cell_value(row, 2, monthx)
                        ws.set_cell_value(row, 3, dayx)
                        ws.set_cell_value(row, 4, utchourx)
                        ws.set_cell_value(row, 5, hourx)

                        if self.hr_or_min == '15MIN':
                            ws.set_cell_value(row, 6, data.get('minute'))
                            ws.set_cell_value(row, 7, data.get('minute_end'))

                        if self.hr_or_min == '1H':
                            ws.set_cell_value(row, 6, data.get('hourx_end'))

                        x_row = 7
                        if self.hr_or_min == '15MIN':
                            x_row = 8
                        ws.get_cell_style(row, x_row).borders.left.color = self.color_border

                    # VARIABLES DYNAMICS
                    cnt_i = 1
                    for channel in self.channels:
                        try:
                            channel_v = data.get('channel_val{}'.format(channel.get('order_field')))
                        except ErrorException:
                            channel_v = 0
                        channel_x = eval('channel_q_{}'.format(cnt_i, ))
                        ws.set_cell_value(row, channel_x, channel_v)
                        ws.get_cell_style(row, channel_x).format.format = '#,##0.00'
                        if cnt_i == self.channel_quantity:
                            ws.get_cell_style(row, channel_x).borders.right.color = self.color_border
                        cnt_i += 1
                    row += 1

                # CREATE VARIABLE DYNAMIC - (AUTO INCREMENT)
                cnt_q = 1
                while self.channel_quantity >= cnt_q:
                    channel_q = eval('channel_q_{}'.format(cnt_q, ))
                    globals()['channel_q_{}'.format(cnt_q, )] = channel_q + self.channel_quantity
                    cnt_q += 1

        wb.save(output)
        return wb

    @staticmethod
    def __get_letter(number):
        """
        GENERATE A-Z or AA-ZZ or AAA-ZZZ, ETC
        :param number:
        :return:
        """
        string = ''
        while number > 0:
            number, remainder = divmod(number - 1, 26)
            string = chr(65 + remainder) + string
        return string


class RegisterCSVHelper(object):
    __slots__ = ['head', 'detail', 'channels', 'channel_quantity', 'hr_or_min', ]

    def __init__(self, head=None, detail=None, channels=None, hr_or_min='1HR', ):

        if channels is None:
            channels = []

        if detail is None:
            detail = []

        if head is None:
            head = []

        self.head = head
        self.detail = detail
        self.channels = channels
        self.channel_quantity = len(channels)
        self.hr_or_min = hr_or_min

    def save(self, response, delimiter=','):
        writer = csv.writer(response, delimiter=delimiter)
        writer.writerow([])
        writer.writerow([])
        writer.writerow([])
        socket_apd = ['', '', '', '', '', '', 'Punto de medida']
        client_apd = ['', '', '', '', '', '', 'Coordinado']
        noins_apd = ['', '', '', '', '', '', 'Serie Medidor']
        user_defined02_apd = ['', '', '', '', '', '', 'Subestación']
        date_last_reading_apd = ['', '', '', '', '', '', 'Fecha Ultima Lectura']
        backup_des_apd = ['', '', '', '', '', '', 'Principal/Respaldo']
        binnacles_apd = ['', '', '', '', '', '', 'ID Bitacora/F-Inicio_F-fin']
        for m in self.head:
            cnt_q = 1
            while self.channel_quantity >= cnt_q:
                socket_apd.append((cnt_q == 2) and m.get('idsocket') or '')
                client_apd.append((cnt_q == 2) and m.get('idclient') or '')
                noins_apd.append((cnt_q == 2) and m.get('noins') or '')
                user_defined02_apd.append((cnt_q == 2) and m.get('user_defined01') or '')
                date_last_reading_apd.append((cnt_q == 2) and m.get('date_last_reading') or '')
                backup_des_apd.append((cnt_q == 2) and m.get('backup_des') or '')
                binnacles_apd.append((cnt_q == 2) and m.get('binnacles') or '')
                cnt_q += 1
        writer.writerow(socket_apd)
        writer.writerow(client_apd)
        writer.writerow(noins_apd)
        writer.writerow(user_defined02_apd)
        writer.writerow(date_last_reading_apd)
        writer.writerow(backup_des_apd)
        writer.writerow(binnacles_apd)
        total_base = ['TOTAL MENSUAL', '', '', '', '', '', '']
        title_base = ['AÑO', 'MES', 'DIA', 'HORA UTC', 'HORA', ]
        if self.hr_or_min == '15MIN':
            title_base.append('MINUTO FIN')
        if self.hr_or_min == '1H':
            title_base.append('HORA FIN')
        title_base.append('')
        data_apd_l = defaultdict(list)
        for k, d in enumerate(self.detail):
            data_apd = self.detail[d]
            for channel in self.channels:
                title_base.append(channel.get('idvar'))
                sum_column = 0
                try:
                    sum_column = round(
                        sum([d.get('channel_val{}'.format(channel.get('order_field'))) for d in data_apd]), 5
                    )
                    sum_column = str(sum_column).replace('.', ',')
                except ErrorException:
                    pass
                total_base.append(sum_column)
            for i, data in enumerate(data_apd):
                yearx = data.get('yearx')
                monthx = data.get('monthx')
                dayx = data.get('dayx')
                hourx = data.get('hourx')
                utchourx = data.get('utchourx')
                time_str = ''
                if self.hr_or_min == '15MIN':
                    time_str = data.get('minute_end')
                if self.hr_or_min == '1H':
                    time_str = data.get('hourx_end')

                if k == 0:
                    data_apd_l[i].append(yearx)
                    data_apd_l[i].append(monthx)
                    data_apd_l[i].append(dayx)
                    data_apd_l[i].append(hourx)
                    data_apd_l[i].append(utchourx)
                    data_apd_l[i].append(time_str)
                    data_apd_l[i].append('')
                # VARIABLES DYNAMICS
                for channel in self.channels:
                    channel_v = ''
                    try:
                        channel_v = round(data.get('channel_val{}'.format(channel.get('order_field'))), 5)
                        channel_v = str(channel_v).replace('.', ',')
                    except ErrorException:
                        pass
                    data_apd_l[i].append(channel_v)
        writer.writerow(total_base)
        writer.writerow(title_base)
        for i in data_apd_l:
            writer.writerow(data_apd_l[i])
        return response
