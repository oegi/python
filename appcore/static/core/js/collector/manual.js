/**
 * @author [Oraima Garcia] <[<  >]>
 * @description [ script collector ]
 * Fecha de creación: 12/12/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */


;(function ($, window, document) {
    'use strict';

    const client = $('[id="client"]');
    const measurement = $('[id="measurement"]');
    const form = $('[id="measu-collector-manual-frm"]');

    if (client.val() !== '' && client.val() !== null) {
        __getMails({
            'idclient': client.val()
        });

        __getMeasurementClient({
            'idclient': client.val()
        });
    }

    client.on('change', function () {
        $('.cn-generate-struct').addClass('hide');
        __getMeasurementClient({'idclient': $(this).val()});
        __getMails({'idclient': $(this).val()});
        __getRefreshTable();
        $('#date-end').val('');
    });

    measurement.on('change', function () {
        const containerGn = $('.cn-generate-struct');
        const lastDateTime = $(this).find('option:selected').data('last_date');

        containerGn.addClass('hide');

        $('#date-last').val(lastDateTime);
        $('#date-end').val('');
        __getLastDate();
        __getRefreshTable();
    });


    $('[id="generate-btn"]').on('click', function (e) {
        e.preventDefault();
        __getFormValidator(form);
        const cnGenerateStruct = $('.cn-generate-struct');
        cnGenerateStruct.addClass('hide');
        if (form.valid()) {
            const data = __getParseForm('measu-collector-manual-frm');
            data['id_soc'] = $('[id="measurement"] option:selected').val();
            data['date_last'] = $('[id="date-last"]').val();
            __loadDataCollector(data);
        }
    });

    $('[id="upload-btn"]').on('click', function (e) {
        e.preventDefault();
        __getFormValidator(form);
        if (form.valid()) {
            console.log(this)
        }
    });

    /**
     * @param data
     * @private
     */
    function __getMeasurementClient(data) {
        let options = '';
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/filter/measurement-socket/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response, status) {
            const data = response.data;
            const measurement = $('[id="measurement"]');
            if (data.length !== 0) {
                $.each(data, function (k, v) {
                    options += `<option value="${v.id_soc}" data-last_date="${v.last_date}">${v.idsocket}</option>`;
                });
            }
            measurement.html(options).formSelect();
            const lastDateTime = measurement.find('option:first').data('last_date');
            if (typeof lastDateTime !== 'undefined') {
                const dateStart = $('#date-last');
                dateStart.val(lastDateTime);
                __getLastDate();
            }
        }).fail(function (response, status) {
            $('[id="measurement"]').html(options).formSelect();
        });
    }

    /**
     * @param data
     * @private
     */
    function __getMails(data) {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/collector/mail/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response, status) {
            const data = response.data;
            $('[id="email"]').val(data.mail_to);
        }).fail(function (response, status) {
            $('[id="email"]').val('');
        });
    }

    /**
     * @param form
     * @private __getFormValidator
     */
    function __getFormValidator(form) {
        form.validate({
            errorElement: 'span',
            errorClass: 'help-inline',
            rules: {
                client: 'required',
                measurement: 'required',
                date_last: 'required',
                interval: 'required',
                date_end: {
                    required: true,
                    date_greater: ["#date-last", '',]
                },
                email: {
                    required: true,
                    multiemails: true,
                },
                message: {
                    required: true,
                    maxlength: 500,
                    minlength: 1
                }
            },
            messages: {
                client: {
                    required: 'Este campo es obligatorio.',
                },
                measurement: {
                    required: 'Este campo es obligatorio.',
                },
                date_last: {
                    required: 'Este campo es obligatorio.',
                },
                date_end: {
                    required: 'Este campo es obligatorio.',
                },
                multiemails: {
                    required: 'Este campo es obligatorio.',
                },
                message: {
                    required: 'Este campo es obligatorio.',
                }
            },
        });
    }

    $('[id="reset-btn"]').on('click', function (e) {
        window.location.reload();
    });

    /**
     * @private __getLastDate()
     */
    function __getLastDate() {
        const dateLast = $('#date-last');
        const dateEnd = $('#date-end');
        if (dateLast.val() !== "" && dateLast.val() !== null) {
            const subStart = moment(dateLast.val(), 'DD-MM-YYYY HH:mm');
            let subEnd = moment(dateLast.val(), 'DD-MM-YYYY HH:mm').endOf('month');

            const monthStart = subStart.format('M');
            const monthNow = subStart.format('M');

            if (monthStart === monthNow) {
                subEnd = moment(moment(), 'DD-MM-YYYY HH:mm')
            }

            dateEnd.bootstrapMaterialDatePickerM({
                lang: 'es',
                format: 'DD-MM-YYYY HH:mm',
            });

            dateEnd.bootstrapMaterialDatePickerM('setMinDate', subStart.toDate());
            dateEnd.bootstrapMaterialDatePickerM('setMaxDate', subEnd.toDate());
        }
    }

    /**
     * @param obj
     * @private
     */
    function __loadDataCollector(obj) {
        const cnGenerateStruct = $('.cn-generate-struct');
        $.ajax({
            url: `/api/table/collector-manual/`,
            method: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            data: JSON.stringify(obj),
        }).done(function (response, status) {
            const columns = response.columns;
            const data = response.data;

            $.each(columns, function (k, d) {
                columns[k]['render'] = function (d, t, r) {
                    const readonly = r.readonly;
                    const iclass = r.class;
                    const classSecondary = r.class_secondary;
                    return (k === 0) ? `<span class="${classSecondary}">${d}</span>`
                        : `<input placeholder="${d}" id="inp_${r.inc + k}" type="text" value="${d}" 
                        class="${iclass}" ${readonly}>`;
                }
            });

            __getRefreshTable();

            const table = $('#table-generate');
            table.DataTable({
                data: data,
                columns: columns,
                createdRow: function (row, data, dataIndex) {
                    $(row).find('td').addClass('mdl-td');
                    $(row).find('td input').addClass('mdl-td-inp');
                    $(row).find('td:eq(1) input').focus();
                }
            }).rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            });

            cnGenerateStruct.removeClass('hide');
        }).fail(function (response, status) {
            if (status === 'error') {
                console.error(response)
            }
        });
    }

    /**
     * @param id
     * @returns {Array}
     * @private fn __getParseForm
     */
    function __getParseForm(id) {
        const data = {};
        $.each($(`[id="${id}"]`).serializeArray(), (k, d) => {
            data[d['name']] = d['value'];
        });
        return data;
    }

    /**
     * @private __getRefreshTable
     */
    function __getRefreshTable() {
        const table = $('#table-generate');

        if ($.fn.DataTable.isDataTable('#table-generate')) {
            table.dataTable().fnDestroy();
        }

        table.html('');
    }
}(jQuery, window, document));