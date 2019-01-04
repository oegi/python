/**
 * @author [Oraima Garcia] <[< >]>
 * @description [ script collector ]
 * Fecha de creación: 30/11/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */


;(function ($, window, document) {
    'use strict';

    const client = $('[id="client"]');
    const measurement = $('[id="measurement"]');
    const form = $('[id="measurement-collector-form"]');

    if (client.val() !== '' && client.val() !== null) {
        __getMails({
            'idclient': client.val()
        });

        __getMeasurementClient({
            'idclient': client.val()
        });
    }

    client.on('change', function () {
        __getMeasurementClient({
            'idclient': $(this).val()
        });

        __getMails({
            'idclient': $(this).val()
        });

        $('#attachment').val('');
        let textName = 'Subir Archivo PRMTE';
        $('[id="text-upload"]').html(textName);
    });

    measurement.on('change', function () {
        const lastDateTime = $(this).find('option:selected').data('last_date');
        $('#date-start').val(lastDateTime);
        loadLastDateTime();
    });

    $('[id="attachment"]').on('change', function (e) {
        let textName = 'Subir Archivo PRMTE';
        if ($(this).val() !== '')
            textName = '&nbsp;' + $(this).val().split('\\').pop();
        $('[id="text-upload"]').html(textName);
    });

    $('[id="send-btn"]').on('click', function (e) {
        e.preventDefault();

        const client = $('#client');
        const measurement = $('#measurement');
        const dateStart = $('#date-start');
        const dateEnd = $('#date-end');
        const email = $('#email');
        const message = $('#message');
        const attachment = $('#attachment');
        const formdata = new FormData();

        formdata.append('client', client.val());
        formdata.append('measurement', measurement.val());
        formdata.append('date_start', dateStart.val());
        formdata.append('date_end', dateEnd.val());
        formdata.append('email', email.val());
        formdata.append('message', message.val());
        formdata.append('attachment', attachment.get(0).files[0]);
        formValidator(form);
        if (form.valid()) {
            const loading = __getDialog('Achivo', 'Espere un momento mientras se procesa el archivo');
            __getAttachamment(formdata, loading);
        }
    });


    /**
     * @param formData
     * @param modal
     * @private fn __getAttachamment
     */
    function __getAttachamment(formData, modal) {
        $.ajax({
            url: `/api/collector/`,
            method: 'POST',
            cache: false,
            processData: false,
            contentType: false,
            data: formData,
        }).done(function (response, status) {
            modal.close();
            $.confirm({
                icon: 'fas fa-check-circle',
                title: '',
                content: response.message,
                theme: 'modern',
                closeIcon: true,
                animation: 'scale',
                type: 'green',
                buttons: {
                    confirm: {
                        text: 'Continuar',
                        btnClass: 'btn-blue btn-xs',
                        action: function () {
                        }
                    },
                }
            });
        }).fail(function (response, status) {
            if (status === 'error') {
                modal.close();
                $.confirm({
                    icon: 'fas fa-times-circle',
                    title: status,
                    content: response.responseJSON.message,
                    theme: 'modern',
                    closeIcon: true,
                    animation: 'scale',
                    type: 'red',
                    buttons: {
                        cancel: {
                            text: 'Cerrar',
                            btnClass: 'btn-xs btn-primary',
                            action: function () {
                            }
                        },
                    }
                });
            }
        });
    }

    /**
     *
     * @param name
     * @param message
     * @returns {jQuery}
     * @private fn __getDialog
     */
    function __getDialog(name, message = 'Espere un momento mientras los datos se cargan...') {
        return $.dialog({
            title: `${name}`,
            closeIcon: false,
            theme: 'modern',
            animation: 'scale',
            closeAnimation: 'zoom',
            columnClass: 'small',
            icon: 'fa fa-cog fa-spin fa-1x fa-fw',
            content: function () {
                let self = this;
                setTimeout(() => {
                    self.setContent(message);
                }, 100);
            },
        });
    }

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
                    options += `<option value="${v.noins}" data-last_date="${v.last_date}">${v.noins}</option>`;
                });
            }
            measurement.html(options).formSelect();
            const lastDateTime = measurement.find('option:first').data('last_date');
            if (typeof lastDateTime !== 'undefined') {
                const dateStart = $('#date-start');
                dateStart.val(lastDateTime);
                loadLastDateTime();
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

    function formValidator(form) {
        form.validate({
            errorElement: 'span',
            errorClass: 'help-inline',
            rules: {
                client: 'required',
                measurement: 'required',
                date_last: 'required',
                date_end: {
                    required: true,
                    date_greater: ["#date-start", '',]
                },
                email: {
                    required: true,
                    multiemails: true
                },
                message: {
                    required: true,
                    maxlength: 500,
                    minlength: 1
                },
                attachment: {
                    required: true,
                    extesion_file: true,
                    name_file: '#measurement',
                    filesize: 5e+6,
                },
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
                },
                attachment: {
                    required: 'Este campo es obligatorio.',
                },
            },
        });
    }

    $('[id="reset-btn"]').on('click', function (e) {
        window.location.reload();
    });

    function loadLastDateTime() {
        const dateLast = $('#date-start');
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
}(jQuery, window, document));