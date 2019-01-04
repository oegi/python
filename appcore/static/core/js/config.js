/**
 * @author [Oraima Garcia]
 * @description [ script config ]
 * Fecha de creación: 08/11/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */
;
(function ($, window, document) {
    const dataTable = $('[id="dt-jquery"]');
    if (dataTable[0]) {
        $.extend($.fn.dataTable.defaults, {
            language: {
                url: dataTable.data('language'),
            },
            paging: true,
            lengthChange: true,
            searching: true,
            ordering: true,
            info: false,
            responsive: true,
            scrollX: true,
            deferRender: true,
            scroller: true,
            pageLength: 10,
            fnInitComplete: function () {
                $('select').formSelect(); //inicializar el select de materialize
            }
        });
        //$.fn.dataTable.ext.classes.sLengthSelect = 'input-field col s12 l6';
    }

    $("#card-alert .alert-closed").click(function () {
        $(this).closest("#card-alert").fadeOut("slow")
    });

    if ($('[id="card-alert"]').is(':visible')) {
        setTimeout(() => {
            $("#card-alert .alert-closed").closest("#card-alert").fadeOut("slow")
        }, 8000);
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            const spinner = $('#sppiner-loading');
            if (typeof spinner[0] !== 'undefined') {
                spinner.show();
            }

            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        complete: function () {
            const spinner = $('#sppiner-loading');
            if (typeof spinner[0] !== 'undefined') {
                spinner.hide();
            }
        }
    });
}(jQuery, window, document));