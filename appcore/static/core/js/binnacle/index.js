/**
 * @author [Oraima Garcia] <[< oraima.garcia@gmail.com >]>
 * @description [ script main ]
 * Fecha de creación: 08/11/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */
//reason-add-btn
;


(function ($, window, document) {


    $('#tb-binnacle').DataTable({
        fnRowCallback: function (nRow, aData, iDisplayIndex) {
            fnRowCallback();
        },
        fnDrawCallback: function (nRow, aData, iDisplayIndex) {
            fnRowCallback();
        },
    });


    $('#search-btn').on('click', function () {
        const period_int = $('#period_int'),
            origin = $('#origin'),
            state = $('#state');
        __getBinnacle({
            'period_int': period_int.val(),
            'origin': origin.val(),
            'state': state.val(),
        });
    });

    /**
     * @param data
     * @private
     */
    function __getFinish(data) {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/binnacle/consult/',
            'method': 'PUT',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response) {
            const status = response.status;
            if (status === 'success') {
                $.alert('Se finalizó de forma exitosa..');
                window.location.href = "/bitacora";
            }
        }).fail(function (response, status) {
        });
    }

    /**
     * @param data
     * @private
     */
    function __getFinishGrabar(data) {

        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/binnacle/firstlist/',
            'method': 'PUT',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response) {
            const status = response.status;
            if (status === 'success') {
                $.alert('Guardado exitosamente.');

            }
        }).fail(function (response, status) {
        });
    }
    
    $('#btn-finalizar').on('click', function (e) {
        e.stopImmediatePropagation();
        const id = $(this).data('id');
        const mante_num = $('#mante-num').val(),
            reason = $('#reason').val(),
            comment = $('#comment').val();
        var text = '';

        if (reason == null || reason.length == 0 || reason == 'undefined' || reason == 'Seleccione la opción') {
            text = " Motivo";


        }
        if (comment == null || comment.length == 0 || comment == 'undefined') {
            text = text + " Comentario";

        }
        if (text != '') {
            text = "Debe completar los campos:" + text;
            $.alert(text);
            return false;
        } else {

            $.confirm({
                theme: 'light',
                boxWidth: '400px',
                useBootstrap: false,
                title: '',
                content: '<div class="text-center">¿Está seguro que desea finalizar?</div>',
                buttons: {
                    accept: {
                        text: 'Aceptar',
                        btnClass: 'btn-blue',
                        action: function () {

                            var data = {
                                'mante_num': mante_num,
                                'reason': reason,
                                'comment': comment,
                                'id': id,
                                'state': "FINALIZADO",
                            };
                            $('#history input[type="text"]:not(.select-dropdown.dropdown-trigger), select')
                                .each((key, ele) => data[$(ele).attr('name')] = $(ele).val());
                            __getFinish(data);
                        }
                    },
                    cancelar: function () {
                    },
                },
            });


        }
    });
    $('#btn-grabar').on('click', function (e) {
        e.stopImmediatePropagation();
        const id = $(this).data('id');
        const mante_num = $('#mante-num').val(),
            reason = $('#reason').val(),
            state = $('#state').val(),
            comment = $('#comment').val();
        __getFinishGrabar({
            'mante_num': mante_num,
            'reason': reason,
            'comment': comment,
            'id': id,
            'state': state,
        });
    });


    /**
     * @param data
     * @private
     */
    function __getBinnacle(data) {
        console.log('getBinnacleDATA', data);
        console.log(data);
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/binnacle/firstlist/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response, status) {
            const data = response.data;
            console.log("oraima1", data);
            const table = $('#tb-binnacle');
            $('select').formSelect();
            $('select').formSelect();
            if ($.fn.DataTable.isDataTable('#tb-binnacle')) {
                table.dataTable().fnDestroy();
            }
            table.DataTable({
                data: data,
                columns: [
                    {
                        render: function (data, type, row) {
                            if (row.origin == "PRMTE") {
                                return `<a data-description=${row.origin} href="${table.data('edit')}?binnacle_id=${row.id}"
                                                data-description="${row.description}"
                                                class="groundsmodify btn btn-xs waves-effect
                                                reason-edit-btn warning-strong">
                                            <i class="material-icons">edit</i>
                                        </a>                                        
                                         <td> 
                                         <button disabled data-delete="${row.id}"
                                                        data-cod_binnacle="${row.cod_binnacle}"
                                                        data-date_rescue="${row.drescue}"
                                                        data-idsocket="${row.idsocket}"
                                                        class="binnacle-delete-btn btn btn-xs waves-effect
                                                                waves-light red">
                                                    <i class="material-icons">delete</i>
                                                </button>`;
                            } else {
                                return `<a data-description=${row.origin} href="${table.data('edit')}?binnacle_id=${row.id}"
                                                data-description="${row.description}"
                                                class="groundsmodify btn btn-xs waves-effect
                                                reason-edit-btn warning-strong">
                                            <i class="material-icons">edit</i>
                                        </a>                                        
                                         <button data-delete="${row.id}"
                                                        data-cod_binnacle="${row.cod_binnacle}"
                                                        data-date_rescue="${row.drescue}"
                                                        data-idsocket="${row.idsocket}"
                                                        class="binnacle-delete-btn btn btn-xs waves-effect
                                                                waves-light red">
                                                    <i class="material-icons">delete</i>
                                                </button>`;
                            }
                        }
                    },
                    {
                        'data': 'cod_binnacle'
                    },
                    {
                        'data': 'idsocket'
                    },
                    {
                        'data': 'drescue'
                    },
                    {
                        'data': 'dstart'
                    },
                    {
                        'data': 'dend'
                    },
                    {
                        'data': 'state'
                    },

                ],
                fnRowCallback: function (nRow, aData, iDisplayIndex) {
                    fnRowCallback();
                },
                fnDrawCallback: function (nRow, aData, iDisplayIndex) {
                    fnRowCallback();
                },
            });

        }).fail(function (response, status) {
        });
    }


    /**
     * @private fn __getTrackingSelected
     */
    function __getTrackingSelected() {
        const dropDownContent = $('ul.dropdown-content');
        dropDownContent.find('li:not(.disabled):first').closest('ul li').click(function (e) {
            const that = this,
                select = $(that).parent().parent().find('select');
            select.find('option').each((k, v) => {
                $(v).prop('selected', $(that).is(':selected'));
            });
            select.formSelect();
            __getTrackingSelected();
        });
    }

    /**
     * @param data
     * @private
     */
    function __getDelete(data) {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/binnacle/firstlist/',
            'method': 'DELETE',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response) {
            const status = response.status;
            if (status === 'success') {
                $.alert('Se ha eliminado correctamente');
                __getBinnacle({
                    'period_int': "",
                    'origin': "",
                    'state': "PENDIENTE",
                });
            }
        }).fail(function (response, status) {
        });
    }


    function fnRowCallback() {

        /*DELETE*/
        $('.binnacle-delete-btn').closest('tr').find('[data-delete]').on('click', function (e) {
            e.stopImmediatePropagation();
            const id = $(this).data('delete');
            const cod_binnacle = $(this).data('cod_binnacle');
            const date = $(this).data('date_rescue');
            const idsocket = $(this).data('idsocket');
            console.log($(this).data());
            console.log(date);
            $.confirm({
                theme: 'light',
                boxWidth: '400px',
                useBootstrap: false,
                title: '',
                content: '<center>¿Está seguro de eliminar la bitácora del día: ' + date + ' y del Socket: ' + idsocket + '?.</center>',
                buttons: {
                    accept: {
                        text: 'Aceptar',
                        btnClass: 'btn-blue',
                        action: function () {

                            __getDelete({
                                'id': id,
                                'cod_binnacle': cod_binnacle,
                            });


                        }
                    },
                    cancelar: function () {
                    },
                },
            });
        });
        /*MODIFY*/
        $('.binnacle-edit-btn').closest('tr').find('[data-edit]').on('click', function (e) {

            e.stopImmediatePropagation();
            const id = $(this).data('edit');
            console.log($(this).data('edit'));
            $.ajax({
                'async': true,
                'crossDomain': true,
                'url': '/api/binnacle/consult/',
                'method': 'POST',
                'headers': {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache',
                },
                'data': JSON.stringify(id),
            }).done(function (response) {

                const data = response.data;
                console.log(data);
                const status = response.status;
                if (status === 'success') {
                    console.log("AJA", data);
                    $('#binnacle_form').html(data);
                    window.location.href = "modificar/";
                    $('#binnacle_form').html(data);

                }
            }).fail(function (response, status) {
            });


        });
    }

    $('[id="btn-reset"]').on('click', function (e) {
        localStorage.removeItem('period_rescue');
        localStorage.removeItem('origin');
        localStorage.removeItem('state');
        window.location.reload();
    });

    setTimeout(function () {
        __getTrackingSelected();
    }, 500);
}(jQuery, window, document));