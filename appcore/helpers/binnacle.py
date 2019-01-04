from appcore.models import Reason
import time, os

from pyexcelerate import (
    Workbook,
    Style,
    Font,
    Alignment,
    Fill,
    Color
)

from appcore.helpers.exceptions import ErrorException


class BinnacleHelper(object):
    __slots__ = ['head', 'detail','color_border',]

    def __init__(self, head=None, detail=None):

        if detail is None:
            detail = []

        if head is None:
            head = []

        self.head = head
        self.detail = detail
        self.color_border = Color(67, 71, 75)

    def save(self, output='/BITACORA/Bitacora.xlsx'):
        datetime_ce = time.strftime("%Y%m%d")
        year = time.strftime("%Y")
        month = time.strftime("%m")
        directory = os.path.join('/BITACORA/', year, month)

        if not os.path.exists(directory):
            os.makedirs(directory)
        output1 ='/BITACORA/'+year+'/'+month+'/Bitacora_'+datetime_ce+'.xlsx'
        wb = Workbook()
        ws = wb.new_sheet('sheet name', data=[])


        factor = 16


        # Hace que sea autoajustable
        ws.set_col_style(1, Style(size=-1, ))
        ws.set_col_style(2, Style(size=-1, ))
        ws.set_col_style(3, Style(size=-1, ))
        ws.set_col_style(5, Style(size=-1, ))
        ws.set_col_style(6, Style(size=-1, ))
        ws.set_col_style(4, Style(size=-1, ))
        ws.set_col_style(7, Style(size=-1, ))
        ws.set_col_style(8, Style(size=-1, ))
        ws.set_col_style(9, Style(size=-1, ))
        ws.set_col_style(10, Style(size=-1, ))
        ws.set_col_style(11, Style(size=-1, ))
        ws.set_col_style(12, Style(size=-1, ))
        ws.set_col_style(13, Style(size=-1, ))
        ws.set_col_style(14, Style(size=-1, ))
        ws.set_col_style(15, Style(size=-1, ))
        ws.set_col_style(16, Style(size=-1, ))
        ws.set_cell_value(1, 1, 'BITACORA')
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

        ws.set_cell_value(2, 1, 'ID_BITACORA', )
        ws.set_cell_value(2, 2, 'ID_DEVICE', )
        ws.set_cell_value(2, 3, 'ID_SOCKET',)
        ws.set_cell_value(2, 4, 'FECHA INI.MEDIDA',)
        ws.set_cell_value(2, 5, 'FECHA FIN MEDIDA',)
        ws.set_cell_value(2, 6, 'FECHA INTERVENCION', )
        ws.set_cell_value(2, 7, 'ORIGEN', )
        ws.set_cell_value(2, 8, 'ESTADO',)
        ws.set_cell_value(2, 9, 'SUBESTACION',)
        ws.set_cell_value(2, 10, 'TENSION',)
        ws.set_cell_value(2, 11, 'PAÑO',)
        ws.set_cell_value(2, 12, 'COORDINADO',)
        ws.set_cell_value(2, 13, 'RESPONSABLE',)
        ws.set_cell_value(2, 14, 'MOTIVO', )
        ws.set_cell_value(2, 15, 'N INTER. MANTE', )
        ws.set_cell_value(2, 16, 'COMENTARIO',)





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
            cod_binnacle = d.get('cod_binnacle')
            noins = d.get('noins')
            idsocket = d.get('idsocket')
            date_start = d.get('date_start').strftime("%d/%m/%Y %H:%M:%S")
            date_end = d.get('date_end').strftime("%d/%m/%Y %H:%M:%S")
            date_rescue = d.get('date_rescue').strftime("%d/%m/%Y %H:%M:%S")
            origin = d.get('origin')
            state = d.get('state')
            substation = d.get('user_defined01')
            tension = d.get('user_defined03')
            panio = d.get('user_defined02')
            coordinado = d.get('idclient')
            responsable = d.get('user')
            mante_num = d.get('mante_num')
            description_reason = d.get('descrip_reason')
            comments = d.get('comments')
            ws.set_cell_value(row, 1, cod_binnacle)
            ws.set_cell_style(row, 1, Style(size=40, ))
            font = Font(bold=False)
            ws[row][1].style.font = font
            ws.set_cell_value(row, 2, noins)
            ws.set_cell_style(row, 2, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 3, idsocket)
            ws.set_cell_style(row, 3, Style(size=-1, ))
            ws[row][2].style.font = font
            ws.set_cell_value(row, 4, date_start)
            ws.set_cell_style(row, 4, Style(size=-1, ))
            ws[row][3].style.font = font
            ws.set_cell_value(row, 5, date_end)
            ws.set_cell_style(row, 5, Style(size=-1, ))
            ws[row][4].style.font = font
            ws.set_cell_value(row, 6, date_rescue)
            ws.set_cell_style(row, 6, Style(size=-1, ))
            ws[row][5].style.font = font
            ws.set_cell_value(row, 7, origin)
            ws.set_cell_style(row, 7, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 8, state)
            ws.set_cell_style(row, 8, Style(size=-1, ))
            ws[row][6].style.font = font
            ws.set_cell_value(row, 9, substation)
            ws.set_cell_style(row, 9, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 10, tension)
            ws.set_cell_style(row, 10, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 11, panio)
            ws.set_cell_style(row, 11, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 12, coordinado)
            ws.set_cell_style(row, 12, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 13, responsable)
            ws.set_cell_style(row, 13, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 14, description_reason)
            ws.set_cell_style(row, 14, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 15, mante_num)
            ws.set_cell_style(row, 15, Style(size=-1, ))
            ws[row][7].style.font = font
            ws.set_cell_value(row, 16, comments)
            ws.set_cell_style(row, 16, Style(size=-1, ))
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
        ws.set_cell_style(1, 1, Style(font=Font(bold=True)))




        ws.set_cell_style(1, 1, Style(fill=Fill(background=Color(143, 180, 236, 0))))
        ws[1][1].style.alignment.horizontal = 'center'

        # Hace que sea autoajustable
        ws.set_col_style(1, Style(size=16 ))
        ws.set_col_style(2, Style(size=25, ))
        ws.set_col_style(3, Style(size=27, ))
        ws.set_col_style(5, Style(size=-1, ))
        ws.set_col_style(6, Style(size=-1, ))
        ws.set_col_style(4, Style(size=-1, ))
        ws.set_col_style(7, Style(size=-1, ))
        ws.set_col_style(8, Style(size=-1, ))
        ws.set_col_style(9, Style(size=-1, ))
        ws.set_col_style(10, Style(size=-1, ))
        ws.set_col_style(11, Style(size=-1, ))
        ws.set_col_style(12, Style(size=-1, ))
        ws.set_col_style(13, Style(size=-1, ))
        ws.set_col_style(14, Style(size=-1, ))
        ws.set_col_style(15, Style(size=-1, ))
        ws.set_col_style(16, Style(size=-1, ))

        wb.save(output)
        wb.save(output1)
        return wb
