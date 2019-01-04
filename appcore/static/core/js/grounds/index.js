/**
 * @author [Oraima Garcia]
 * @description [ script main ]
 * Fecha de creación: 08/11/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */
;


(function ($, window, document) {

    $('#tb-grounds').DataTable({
        fnRowCallback: function (nRow, aData, iDisplayIndex) {
            fnRowCallback();
        },
    });


    /**
     * @param data
     * @private
     */
    function __getModify(data) {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/reason/',
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
                __getReasons();
            }
        }).fail(function (response, status) {
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
            'url': '/api/reason/',
            'method': 'DELETE',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response) {
            const status = response.status;
            if (status === 'success') {
                 $.alert('Motivo Eliminado con Exito');
                __getReasons();
            }else{
                $.alert('Este Motivo no se puede eliminar, está siendo usado en Bitacoras');
            }
        }).fail(function (response, status) {
        });
    }


     /**
     * @param data
     * @private
     */
    function __getAdd(data) {
        console.log("data", data);
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/reason/create/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(data),
        }).done(function (response) {
            const status = response.status;
            if (status === 'success') {
                $.alert('Guardado exitosamente.');
                __getReasons();
            }
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
     * @returns {*}
     * @private
     */
    function __getReasons() {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/reason/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
        }).done(function (response,) {
            const status = response.status;
            const data = response.data;
              console.log(data);
            if (status === 'success') {

                const table = $('#tb-grounds');
                if ($.fn.DataTable.isDataTable('#tb-grounds')) {
                    table.dataTable().fnDestroy();
                }

                table.DataTable({
                    data: data,
                    columns: [
                         {
                            render: function (data, type, row) {
                                return `<button data-edit="${row.id}"
                                                data-description="${row.description}"
                                                class="groundsmodify btn btn-xs waves-effect
                                                reason-edit-btn warning-strong">
                                            <i class="material-icons">edit</i>
                                        </button>
                                         <button data-delete="${row.id}"
                                                 data-description="${row.description}"
                                                 class="reason-delete-btn btn btn-xs waves-effect waves-light red">
                                             <i class="material-icons">delete</i>
                                         </button>`
                            }
                        },
                        {
                            'data': 'description'
                        },
                        {
                            'data': 'date_created'
                        },

                    ],
                    fnRowCallback: function (nRow, aData, iDisplayIndex) {
                        fnRowCallback();
                    },
                    drawCallback: function () {
                        fnRowCallback();
                    }
                });
            }
        }).fail(function (response, status) {
        });
    }



    function fnRowCallback() {
        /*DELETE*/
        $('.reason-delete-btn').closest('tr').find('[data-delete]').on('click', function (e) {
            e.stopImmediatePropagation();
            const id = $(this).data('delete');
            const description = $(this).data('description');
            console.log($(this).data());
            console.log(description);
            $.confirm({
                theme: 'light',
                boxWidth: '300px',
                useBootstrap: false,
                title: '¿Esta seguro que desea eliminar el motivo?',
                content: `${description}`,
                buttons: {
                    accept: {
                        text: 'Aceptar',
                        btnClass: 'btn-blue',
                        action: function () {
                            __getDelete({
                                'is_active': false,
                                'description': description,
                                'id': id,
                            });
                        }
                    },
                    cancelar: function () {
                    },
                },
            });
        });
        /*MODIFY*/
        $('.reason-edit-btn').closest('tr').find('[data-edit]').on('click', function (e) {
            e.stopImmediatePropagation();
            const id = $(this).data('edit');
            const description = $(this).data('description');
            $.confirm({
                theme: 'light',
                boxWidth: '300px',
                useBootstrap: false,
                title: 'Modificar Motivo',
                content: `<form id="reason-form" class="formName">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col s11">
                                                <input type="text" name="description_edit" placeholder="MOTIVO" 
                                                value="${description}" class="name form-control" required/>
                                            </div>
                                        </div>
                                    </div>
                               </form>`,
                buttons: {
                    accept: {
                        text: 'Aceptar',
                        btnClass: 'btn-blue',
                        action: function () {
                            const form = $('[id="reason-form"]');
                            if (form.valid()) {
                                __getModify({
                                    'is_active': true,
                                    'description': $('[name="description_edit"]').val(),
                                    'id': id,
                                });
                                return true;
                            }
                            return false;
                        }
                    },
                    cancelar: function () {
                    },
                },
            });
        });

        /*ADD*/
        $('.reason-add-btn').on('click', function (e) {

            e.stopImmediatePropagation();
            $.confirm({
                theme: 'light',
                boxWidth: '300px',
                useBootstrap: false,

                title: 'Agrega un Nuevo Motivo',
                ///title: 'Registro PRMTE!',
               content: `<form id="reason-form" class="formName">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col s11">
                                                <input id="id_motivo" type="text" name="description_edit" placeholder="MOTIVO" 
                                                 class="name form-control" required/>
                                            </div>
                                        </div>
                                    </div>
                               </form>`,
                    buttons: {
                    accept: {
                        text: 'Aceptar',
                        btnClass: 'btn-blue',
                        action: function () {
                            const form = $('[id="reason-form"]');
                            console.log($("#id_motivo").val());
                            if (form.valid()) {
                                __getAdd({
                                    'is_active': true,
                                    'description': $("#id_motivo").val(),
                                   // 'id': id,
                                });

                                return true;



                            }
                            return false;
                        }
                    },
                    cancelar: function () {
                    },
                },
            });
        });
    }

    setTimeout(function () {
        __getTrackingSelected();
    }, 500);
}(jQuery, window, document));