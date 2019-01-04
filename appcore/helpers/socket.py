from appcore.models import Reason
import time

from pyexcelerate import (
    Workbook,
    Style,
    Font,
    Alignment,
    Fill,
    Color
)

from appcore.helpers.exceptions import ErrorException


class SocketHelper(object):
    __slots__ = ['head', 'detail','color_border',]

    def __init__(self, head=None, detail=None):

        if detail is None:
            detail = []

        if head is None:
            head = []

        self.head = head
        self.detail = detail
        self.color_border = Color(67, 71, 75)

    def save(self, output='/SOCKET/'+time.strftime("%Y")+'/Socket_Channel'+ time.strftime("%d%m%Y") +'.xlsx'):
        output1 = '/SOCKET/SOCKET_HABILITADO.xlsx'
        wb = Workbook()
        ws = wb.new_sheet('sheet name', data=[])
        factor = 33
        # Hace que sea autoajustable

        ws.set_cell_value(1, 1, 'SOCKET_CHANNEL')
        style = Style(font=Font(bold=True), alignment=Alignment(vertical='center', horizontal='center'))
        ws.set_cell_style(1, 1, style)
        ws.set_cell_style(1, 1, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 1, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 2, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 3, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 4, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 5, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 6, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 7, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(1, 8, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 9, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 10, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 11, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 12, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 13, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 14, Style(fill=Fill(background=Color(143, 180, 236, 0))))

        font = Font(bold=True)
        ws[1][1].style.font = font
        ws[1][1].style.alignment.horizontal = 'center'

        ws.range((1, 1), (1, factor)).merge()

        ws.set_cell_value(2, 1, 'id_soc', )
        ws.set_cell_value(2, 2, 'noins', )
        ws.set_cell_value(2, 3, 'idsocket',)
        ws.set_cell_value(2, 4, 'idclient',)
        ws.set_cell_value(2, 5, 'serialno',)
        ws.set_cell_value(2, 6, 'user_defined01', )
        ws.set_cell_value(2, 7, 'user_defined02', )
        ws.set_cell_value(2, 8, 'user_defined03',)
        ws.set_cell_value(2, 9, 'user_defined06',)
        ws.set_cell_value(2, 10, 'user_defined07',)
        ws.set_cell_value(2, 11, 'user_defined14',)
        ws.set_cell_value(2, 12, 'user_defined17',)
        ws.set_cell_value(2, 13, 'user_defined18',)
        ws.set_cell_value(2, 14, 'min_datetime', )
        ws.set_cell_value(2, 15, 'max_datetime', )
        ws.set_cell_value(2, 16, 'user_defined59',)

        ws.set_cell_value(2, 17, 'num_log', )
        ws.set_cell_value(2, 18, 'in_energia_act', )
        ws.set_cell_value(2, 19, 're_energia_act', )
        ws.set_cell_value(2, 20, 'in_energia_rea', )
        ws.set_cell_value(2, 21, 're_energia_rea', )
        ws.set_cell_value(2, 22, 'kwhd', )
        ws.set_cell_value(2, 23, 'kvarhd', )
        ws.set_cell_value(2, 24, 'kwhr', )
        ws.set_cell_value(2, 25, 'kvarhr', )
        ws.set_cell_value(2, 26, 'vll_ab_mean', )
        ws.set_cell_value(2, 27, 'vll_bc_mean', )
        ws.set_cell_value(2, 28, 'vll_ca_mean', )
        ws.set_cell_value(2, 29, 'ia_mean', )
        ws.set_cell_value(2, 30, 'ib_mean', )
        ws.set_cell_value(2, 31, 'ic_mean', )
        ws.set_cell_value(2, 32, 'vll_avg_mean', )
        ws.set_cell_value(2, 33, 'iavg_mean', )

        # bold para ID_BITACORA, Socket, Fecha Intervencion, fecha inicio Medida, fecha fin , estado
        style = Style(font=Font(bold=True), alignment=Alignment(vertical='center', horizontal='center'))
        ws.set_cell_style(2, 1, style)
        ws.set_cell_style(2, 2, style)
        ws.set_cell_style(2, 3, style)
        ws.set_cell_style(2, 4, style)
        ws.set_cell_style(2, 5, style)
        ws.set_cell_style(2, 6, style)
        ws.set_cell_style(2, 7, style)
        ws.set_cell_style(2, 8, style)
        ws.set_cell_style(2, 9, style)
        ws.set_cell_style(2, 10, style)
        ws.set_cell_style(2, 11, style)
        ws.set_cell_style(2, 12, style)
        ws.set_cell_style(2, 13, style)
        ws.set_cell_style(2, 14, style)
        ws.set_cell_style(2, 15, style)
        ws.set_cell_style(2, 16, style)

        data = self.detail
        row = 3  # A partir de aca comienzo a pintar
        for d in data:
            id_soc = d.get('id_soc')
            noins = d.get('noins')
            idsocket = d.get('idsocket')
            idclient = d.get('idclient')
            serialno = d.get('serialno')
            user_defined01 = d.get('user_defined01')
            user_defined02 = d.get('user_defined02')
            user_defined03 = d.get('user_defined03')
            user_defined06 = d.get('user_defined06')
            user_defined07 = d.get('user_defined07')
            user_defined14 = d.get('user_defined14')
            user_defined17 = d.get('user_defined17')
            user_defined18 = d.get('user_defined18')
            min_datetime = d.get('min_datetime').strftime("%d/%m/%Y %H:%M:%S")
            max_datetime = d.get('max_datetime').strftime("%d/%m/%Y %H:%M:%S")
            user_defined59 = d.get('user_defined59')
            num_log = d.get('num_log')
            in_energia_act = d.get('in_energia_act')
            re_energia_act = d.get('re_energia_act')
            in_energia_rea = d.get('in_energia_rea')
            re_energia_rea= d.get('re_energia_rea')
            kwhd = d.get('kwhd')
            kvarhd = d.get('kvarhd')
            kwhr = d.get('kwhr')
            kvarhr = d.get('kvarhr')
            vll_ab_mean = d.get('vll_ab_mean')
            vll_bc_mean = d.get('vll_bc_mean')
            vll_ca_mean = d.get('vll_ca_mean')
            ia_mean = d.get('ia_mean')
            ib_mean = d.get('ib_mean')
            ic_mean = d.get('ic_mean')
            vll_avg_mean = d.get('vll_avg_mean')
            iavg_mean = d.get('iavg_mean')

            ws.set_cell_value(row, 1, id_soc)
            ws.set_cell_style(row, 1, Style(size=-1, ))
            font = Font(bold=False)
            ws[row][1].style.font = font
            ws.set_cell_value(row, 2, noins)
            ws.set_cell_style(row, 2, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 3, idsocket)
            ws.set_cell_style(row, 3, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 4, idclient)
            ws.set_cell_style(row, 4, Style(size=-1, ))
            ws[row][3].style.font = font
            ws.set_cell_value(row, 5, serialno)
            ws.set_cell_style(row, 5, Style(size=-1, ))
            ws[row][4].style.font = font
            ws.set_cell_value(row, 6, user_defined01)
            ws.set_cell_style(row, 6, Style(size=-1, ))
            ws[row][5].style.font = font
            ws.set_cell_value(row, 7, user_defined02)
            ws.set_cell_style(row, 7, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 8, user_defined03)
            ws.set_cell_style(row, 8, Style(size=-1, ))
            ws[row][6].style.font = font
            ws.set_cell_value(row, 9, user_defined06)
            ws.set_cell_style(row, 9, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 10, user_defined07)
            ws.set_cell_style(row, 10, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 11, user_defined14)
            ws.set_cell_style(row, 11, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 12, user_defined17)
            ws.set_cell_style(row, 12, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 13, user_defined18)
            ws.set_cell_style(row, 13, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 14, min_datetime)
            ws.set_cell_style(row, 14, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 15, max_datetime)
            ws.set_cell_style(row, 15, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 16, user_defined59)
            ws.set_cell_style(row, 16, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 17, num_log)
            ws.set_cell_style(row, 17, Style(size=-1, ))
            font = Font(bold=False)
            ws[row][1].style.font = font
            ws.set_cell_value(row, 18, in_energia_act)
            ws.set_cell_style(row, 18, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 19, re_energia_act)
            ws.set_cell_style(row, 19, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 20, in_energia_rea)
            ws.set_cell_style(row, 20, Style(size=-1, ))
            ws[row][3].style.font = font
            ws.set_cell_value(row, 21, re_energia_rea)
            ws.set_cell_style(row, 21, Style(size=-1, ))
            ws[row][4].style.font = font
            ws.set_cell_value(row, 22, kwhd)
            ws.set_cell_style(row, 22, Style(size=-1, ))
            ws[row][5].style.font = font
            ws.set_cell_value(row, 23, kvarhd)
            ws.set_cell_style(row, 23, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 24, kwhr)
            ws.set_cell_style(row, 24, Style(size=-1, ))
            ws[row][6].style.font = font
            ws.set_cell_value(row, 25, kvarhr)
            ws.set_cell_style(row, 25, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 26, vll_ab_mean)
            ws.set_cell_style(row, 26, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 27, vll_bc_mean)
            ws.set_cell_style(row, 27, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 28, vll_ca_mean)
            ws.set_cell_style(row, 28, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 29, ia_mean)
            ws.set_cell_style(row, 29, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 30, ib_mean)
            ws.set_cell_style(row, 30, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 31, ic_mean)
            ws.set_cell_style(row, 31, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 32, vll_avg_mean)
            ws.set_cell_style(row, 32, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 33, iavg_mean)
            ws.set_cell_style(row, 33, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.get_cell_style(row, factor).borders.right.color = self.color_border
            row1 =row
            row += 1
        ws.get_cell_style(row1, 1).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 2).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 3).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 4).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 5).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 6).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 7).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 8).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 9).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 10).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 11).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 12).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 13).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 14).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 15).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 16).borders.bottom.color = self.color_border

        ws.get_cell_style(row1, 17).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 18).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 19).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 20).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 21).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 22).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 23).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 24).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 25).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 26).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 27).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 28).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 29).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 30).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 31).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 32).borders.bottom.color = self.color_border
        ws.get_cell_style(row1, 33).borders.bottom.color = self.color_border


        ws.set_cell_style(2, 1, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 2, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 3, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 4, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 5, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 6, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 7, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 8, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 9, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 10, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 11, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 12, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 13, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 14, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 15, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 16, Style(fill=Fill(background=Color(143, 180, 236, 0))))

        ws.set_cell_style(2, 17, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 18, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 19, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 20, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 21, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 22, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 23, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 24, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 25, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 26, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 27, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 28, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 29, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 30, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 31, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 32, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(2, 33, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws.set_cell_style(1, 1, Style(font=Font(bold=True)))




        ws.set_cell_style(1, 1, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws[1][1].style.alignment.horizontal = 'center'




        wb.save(output)
        wb.save(output1)
        return wb
