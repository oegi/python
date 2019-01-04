$(document).ready(function () {



    $('.login').on('click', function () {
        $.confirm({
            theme: 'light',
            boxWidth: '300px',
            useBootstrap: false,
            icon: 'fa fa-spinner fa-spin',
            title: 'Conectate!',
            ///title: 'Registro PRMTE!',
            content: '' +
                '<form action="" class="formName">' +
                '<div class="form-group">' +
                '<div class="row"><div class="col s11"><input type="text" placeholder="Nombre de Usuario" class="name form-control" required/></div></div>' +
                '<div class="row"><div class="col s11"><input type="password" placeholder="Contraseña" class="pass form-control" required/></div></div>' +
                '</div>' +
                '</form>',
            buttons: {
                formSubmit: {
                    text: 'Aceptar',
                    btnClass: 'btn-blue',
                    action: function () {
                        var name = this.$content.find('.name').val();
                        if (!name) {

                            $.alert('Usuario no valido');
                            return false;
                        }
                        var pass = this.$content.find('.pass').val();

                        if (!pass) {
                            $.alert('Ingrese Contraseña');
                            return false;
                        }
                        location.href = '/#/';

                        $('.cen_btn-empresas').css("background-color", "green");
                        $("p.login").html("<strong>Salir de PRMTE</strong>");

                    }
                },
                cancelar: function () {
                    //close
                },
            },
            onContentReady: function () {
                // you can bind to the form
                var jc = this;
                this.$content.find('form').on('submit', function (e) { // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                });
            }
        });
    });


    if ($('.datepicker')[0]) {
        $('.datepicker').datepicker();
    }
    /***********logo effect********************/
    var pathname = window.location.pathname;
    if (pathname != '/') {

        $(".container").removeClass("matenav").addClass("container");
        $('nav img').css("margin-top", "0px");
        $('nav img').css("width", "90px");
    }


    /*************Parallax************** */
    $('.parallax').parallax();
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.inp-cls').characterCounter();

    $('.sidenav').sidenav();

    $('select').formSelect();

    /**************jconfirm login********** */

    $('.example2-2').on('click', function () {
        $.confirm({
            theme: 'light',
            boxWidth: '300px',
            useBootstrap: false,
            icon: 'fa fa-spinner fa-spin',
            title: 'Conectate!',
            ///title: 'Registro PRMTE!',
            content: '' +
                '<form action="" class="formName">' +
                '<div class="form-group">' +
                '<div class="row"><div class="col s11"><input type="text" placeholder="Nombre de Usuario" class="name form-control" required/></div></div>' +
                '<div class="row"><div class="col s11"><input type="password" placeholder="Contraseña" class="pass form-control" required/></div></div>' +
                '</div>' +
                '</form>',
            buttons: {
                formSubmit: {
                    text: 'Aceptar',
                    btnClass: 'btn-blue',
                    action: function () {
                        var name = this.$content.find('.name').val();
                        if (!name) {

                            $.alert('Usuario no valido');
                            return false;
                        }
                        var pass = this.$content.find('.pass').val();
                        if (!pass) {
                            $.alert('Ingrese Contraseña');
                            return false;
                        }
                        location.href = '/recolector/'
                    }
                },
                cancelar: function () {
                    //close
                },
            },
            onContentReady: function () {
                // you can bind to the form
                var jc = this;
                this.$content.find('form').on('submit', function (e) { // if the user submits the form by pressing enter in the field.
                    e.preventDefault();
                    jc.$$formSubmit.trigger('click'); // reference the button and click it
                });
            }
        });
    });
});

$(window).scroll(function () {
    var pathname = window.location.pathname;
    if (pathname == '/') {
        if (window.pageYOffset >= 100) {
            $(".matenav").removeClass("container").addClass(".matenav");
            $('nav img').css("margin-top", "0px").css("width", "90px");
        } else {
            $('nav img').css("width", "170px");
            $(".matenav").addClass("container");
        }
    } else {
        $(".container").removeClass("matenav").addClass("container");
        $('nav img').css("margin-top", "0px").css("width", "90px");
    }
});






