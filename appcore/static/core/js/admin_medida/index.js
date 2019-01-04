
;
(function ($, window, document) {


     /*************SWITCHE on off***********/

      $(".switch").find("input[type=checkbox]").on("change",function() {
      var checked = $(this).prop('checked');
      let id = $(this).data('id');

      console.log(id, checked);

      if(checked) {
            $.confirm({
                title: 'Activar!',
                content: 'Desea Activar este punto de Medida!',
                buttons: {
                    confirmar: function () {
                        $.alert('Punto de Medida activo!');
                        /*dejar esto en checked*/
                    },
                    cancelar: function () {
                        $.alert('Canceled!');
                        /*desactivar el checked*/
                        $(this).prop('checked', false);
                    }

                }
            });
        } else {
            console.log("entra en elseeeeeeeeeeeeee");
            $.confirm({
                title: 'Desactivar!',
                content: 'Desea Desactivar este punto de Medida!',
                buttons: {
                    confirmar: function () {
                        $.alert('Punto de Medida Inactivo!');
                        /*dejar esto en checked*/
                    },
                    cancelar: function () {
                        $.alert('Punto de medida activo!');
                        /*desactivar el checked*/
                    }

                }
            });
        }


      /*
      $.ajax({
          url: 'http://localhost/conexion/controllers/updatestate',
          type: 'POST',
          data: {'id': id, 'checked' : checked}
      })
      .done(function(resp) {
          console.log(resp);
      })
      .fail(function() {
          console.log("error");
      });
      */

  });




    $('#measure-admin').DataTable();


    $('[id="client"]').on('change', function () {
        __getSubstation({
            'idclient': $(this).val()
        });
    });

    $('[id="substation"]').on('change', function () {
        if ($(this).find('option:not([value="__all__"]):selected')[0] === undefined) {
            const substations = __getParseData($(this).find('option:not([value="__all__"])'));
            $('[id="substation_hidden"]').val(substations.join(','));
        } else {
            const substations = __getParseData($(this).find('option:not([value="__all__"]):selected'));
            $('[id="substation_hidden"]').val(substations.join(','));
        }
    });

    $('[id="btn-reset"]').on('click', function (e) {
        window.location.reload();
    });

    /**
     * @param data
     * @private
     */
    function __getSubstation(data) {
        let options = '<option value="__all__" data-query="__all__">Todos</option>';
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/filter/substation/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),x
        }).done(function (response, status) {
            const data = response.data,
                substationSlt = $('[id="substation"]');
            if (data.length !== 0) {
                $.each(data, function (k, v) {
                    options += `<option value="${v.user_defined01}">${v.user_defined01}</option>`;
                });
            }
            substationSlt.html(options).formSelect();
            __getTrackingSelected();
        }).fail(function (response, status) {
            $('[id="substation"]').html(options).formSelect();
        });
    }
//todo
    $('#search-btn').on('click', function () {
        const client = $('#client'),
            substation = $('#substation_hidden');
        __getMeasurement({
            'idclient': client.val(),
            'substation': substation.val(),
        });
    });


    /**
     * @param data
     * @private
     */
    function __getMeasurement(data) {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/admin/measurement/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response, status) {
            const data = response.data;
            const table = $('#measure-admin');
            if ($.fn.DataTable.isDataTable('#measure-admin')) {
                table.dataTable().fnDestroy();
            }
            table.DataTable({
                data: data,
                columns: [
                    {
                        'data': 'idsocket'
                    },
                    {
                        'data': 'is_active',
                        render: function (data, type, row) {
                            console.log(data, row)
                            return `<div class="switch">
                                        <label>
                                            Inactivo<input type="checkbox">
                                            <span class="lever"></span>Activo
                                        </label>
                                    </div>`
                        }
                    },
                ]
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
     * @param element
     * @returns {*}
     * @private
     */
    function __getParseData(element) {
        return element.map((k, opt) => {
            return $(opt).val();
        }).get();
    }

    setTimeout(function () {
        __getTrackingSelected();
    }, 500);
}(jQuery, window, document));