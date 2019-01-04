/**
 * @author [Oraima Garcia] <[< >]>
 * @description [ script main ]
 * Fecha de creación: 08/11/2018
 * Fecha de actualización:
 * Participantes: [ ]
 */

;
(function ($, window, document) {
    // ALLOWED 4089 CHARACTER FOR COOKIES
    __getLoadLocalStorage();

    $('#months').on('change', function () {
        localStorage.setItem('month', $(this).val());
    });

    $('[name="hr_or_min"]').on('click', function () {
        localStorage.setItem('hr_or_min', $(this).val());
    });

    $('[name="type_file"]').on('click', function () {
        localStorage.setItem('type_file', $(this).val());
    });

    $('[id="btn-reset"]').on('click', function (e) {
        localStorage.removeItem('idclient');
        localStorage.removeItem('substation');
        localStorage.removeItem('level_tension');
        localStorage.removeItem('measurement_point');
        localStorage.removeItem('month');
        localStorage.removeItem('hr_or_min');
        localStorage.removeItem('type_file');
        window.location.reload();
    });

    $('[id="client"]').on('change', function () {
        localStorage.removeItem('substation');
        localStorage.removeItem('level_tension');
        localStorage.removeItem('measurement_point');
        $('#sppiner-loading').show();
        $('#btn-reset, #download-btn').addClass('disabled');
        __getSubstation({
            'idclient': $(this).val()
        });
        localStorage.setItem('idclient', $(this).val());
    });

    $('[id="substation"]').on('change', function () {
        const substationHidden = $('[id="substation_hidden"]');
        localStorage.removeItem('level_tension');
        localStorage.removeItem('measurement_point');
        $('#sppiner-loading').show();
        $('#btn-reset, #download-btn').addClass('disabled');

        if (typeof $('[id="substation"] option[value="__all__"]:selected')[0] !== 'undefined') {
            const substations = __getParseData($(this).find('option:not([value="__all__"])'));
            __getLevelTension({
                'idclient': $('#client').val(),
                'user_defined01': substations,
            });
            substationHidden.val(substations.join(','));
        } else {
            let substations = __getParseData($(this).find('option:not([value="__all__"]):selected'));

            if (0 === substations.length) {
                substations = __getParseData($(this).find('option:not([value="__all__"])'));
            }
            __getLevelTension({
                'idclient': $('#client').val(),
                'user_defined01': substations
            });
            substationHidden.val(substations.join(','));
        }
    });

    $('[id="level-tension"]').on('change', function () {
        const levelTension = $('[id="level_tension_hidden"]');
        localStorage.removeItem('level_tension');
        localStorage.removeItem('measurement_point');
        $('#sppiner-loading').show();
        $('#btn-reset, #download-btn').addClass('disabled');

        if (typeof $('[id="level-tension"] option[value="__all__"]:selected')[0] !== 'undefined') {
            const levelTensions = __getParseData($(this).find('option:not([value="__all__"])'));
            const substationInp = $('#substation');
            let substations = __getParseData(substationInp.find('option:not([value="__all__"]):selected'));
            if (0 === substations.length) {
                substations = __getParseData(substationInp.find('option:not([value="__all__"])'));
            }
            __getMeasurementPoint({
                'idclient': $('#client').val(),
                'user_defined01': substations,
                'user_defined03': levelTensions
            });
            levelTension.val(levelTensions.join(','));
        } else {
            const substationInp = $('#substation');

            let levelTensions = __getParseData($(this).find('option:not([value="__all__"]):selected'));
            let substations = __getParseData(substationInp.find('option:not([value="__all__"]):selected'));

            if (0 === substations.length) {
                substations = __getParseData(substationInp.find('option:not([value="__all__"])'));
            }

            if (0 === levelTensions.length) {
                levelTensions = __getParseData($(this).find('option:not([value="__all__"])'));
            }

            __getMeasurementPoint({
                'idclient': $('#client').val(),
                'user_defined01': substations,
                'user_defined03': levelTensions
            });
            levelTension.val(levelTensions.join(','));
        }
    });

    $('[id="measurement-point"]').on('change', function () {
        localStorage.removeItem('measurement_point');
        const measurementPoint = $('[id="measurement_point_hidden"]');
        if (typeof $('[id="measurement-point"] option[value="__all__"]:selected')[0] !== 'undefined') {
            const levelTensions = __getParseData($(this).find('option:not([value="__all__"])'));
            measurementPoint.val(levelTensions.join(','));
            localStorage.setItem('measurement_point', levelTensions);
        } else {
            const levelTensions = __getParseData($(this).find('option:not([value="__all__"]):selected'));
            measurementPoint.val(levelTensions.join(','));
            localStorage.setItem('measurement_point', measurementPoint.val());
        }
        __getPointReload();
    });

    /**
     * @param dataElements
     * @private
     */
    function __getSubstation(dataElements) {
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
            'data': JSON.stringify(dataElements),
        }).done(function (response, status) {
            const data = response.data,
                substationSlt = $('[id="substation"]');
            if (data.length !== 0) {
                $.each(data, function (k, v) {
                    options += `<option value="${v.user_defined01}">${v.user_defined01}&nbsp;(${v.dcount})</option>`;
                });
            }

            substationSlt.html(options).formSelect();
            let substationRs = data.map((v, k) => {
                return v.user_defined01
            });

            let substation = localStorage.getItem('substation');
            if (substation !== null) {
                substationSlt.val(substation.split(',')).formSelect();
                substationRs = substation.split(',');
            }

            const substationInp = $('[id="substation_hidden"]');
            substationInp.val(substationRs.join(','));

            __getLevelTension({
                'idclient': dataElements['idclient'],
                'user_defined01': substationRs,
            });
            __getTrackingSelected();
        }).fail(function (response, status) {
            $('[id="substation"]').html(options).formSelect();
        });
    }

    /**
     * @param dataElements
     * @private
     */
    function __getLevelTension(dataElements) {
        let options = '<option value="__all__" data-query="__all__">Todos</option>';
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/filter/level-tension/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(dataElements),
        }).done(function (response, status) {
            const data = response.data;
            const levelTensionSlt = $('[id="level-tension"]');
            if (data.length !== 0) {
                $.each(data, function (k, v) {
                    options += `<option value="${v.user_defined03}">${v.user_defined03}</option>`;
                });
            }

            levelTensionSlt.html(options).formSelect();

            const substationInp = $('#substation');
            let subtationRs = __getParseData(substationInp.find('option:not([value="__all__"]):selected'));
            if (0 === subtationRs.length) {
                subtationRs = __getParseData(substationInp.find('option:not([value="__all__"])'));
            }

            let levelTensionRs = data.map((v, k) => {
                return v.user_defined03
            });

            const levelTension = localStorage.getItem('level_tension');
            if (levelTension !== null) {
                levelTensionSlt.val(levelTension.split(',')).formSelect();
                levelTensionRs = levelTension.split(',');
            }

            const levelTensionInp = $('[id="level_tension_hidden"]');
            levelTensionInp.val(levelTensionRs.join(','));

            __getMeasurementPoint({
                'idclient': dataElements['idclient'],
                'user_defined01': subtationRs,
                'user_defined03': levelTensionRs
            });
            __getTrackingSelected();
        }).fail(function (response, status) {
            $('[id="level-tension"]').html(options).formSelect();
        });
    }

    /**
     * @param dataElements
     * @private
     */
    function __getMeasurementPoint(dataElements) {
        let options = '<option value="__all__" data-query="__all__">Todos</option>';
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/filter/measurement-point/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify(dataElements),
        }).done(function (response, status) {
            const data = response.data;
            const measurementSlt = $('[id="measurement-point"]');
            if (data.length !== 0) {
                $.each(data, function (k, v) {
                    options += `<option value="${v.idsocket}">${v.idsocket}</option>`;
                });
            }
            measurementSlt.html(options).formSelect();
            measurementSlt.data('measurement_point', data.length);

            dataElements['idsocket'] = data.map((v, k) => {
                return v.idsocket
            });

            const measurementPoint = localStorage.getItem('measurement_point');
            if (measurementPoint !== null) {
                measurementSlt.val(measurementPoint.split(',')).formSelect();
            }

            let measurement_point_s = localStorage.getItem('measurement_point');

            if (measurement_point_s === null && measurementSlt.val() !== null) {
                measurement_point_s = data.map((v, k) => {
                    return v.idsocket
                }).join(',');
            }

            $('[id="measurement_point_hidden"]').val(measurement_point_s);

            setTimeout(() => {
                $('#btn-reset, #download-btn').removeClass('disabled');
                $('#sppiner-loading').hide();
                __getTrackingSelected();
                __setLoadLocalStorage();
                __getPointReload();
            }, 500);
        }).fail(function (response, status) {
            $('[id="measurement-point"]').html(options).formSelect();
        });
    }

    const formRegister = $('#form-register');
    document.getElementById('download-btn').addEventListener('click', function (e) {
        e.preventDefault();

        const client = $('[id="client"]');
        const substation = $('[id="substation"]');
        const levelTension = $('[id="level-tension"]');
        const quantityPointsDb = $('[id="quantity-points-db"]').data('points');
        let measurementPoint = $('[id="measurement-point"]');
        let measurementPointL = measurementPoint.data('measurement_point');
        let measurementPointH = measurementPoint.find('option:not([value="__all__"]):selected').length;

        const formRC = document.getElementById('form-register');
        const massivePoint = $('[id="massive-point"]');
        if (typeof massivePoint[0] !== 'undefined') {
            massivePoint.remove();
        }

        if ('__all__' !== client.val() && substation.val() === null
            && levelTension.val() === null && measurementPointL === measurementPointH
            && quantityPointsDb < measurementPointL) {
            const input = document.createElement('input');
            input.setAttribute('id', 'massive-point');
            input.setAttribute('name', 'massive_point');
            input.setAttribute('type', 'hidden');
            input.setAttribute('value', 'MASSIVE_POINT');
            formRC.appendChild(input);
        }

        const that = this;
        const btnReset = $('#btn-reset');

        formRegister.submit();
        $(that).addClass('disabled');
        btnReset.addClass('disabled');
        setCookie('register_response', '');
        $('#sppiner-loading').show();

        const intervalInit = setInterval(function () {
            if (getCookie('register_response') === 'success') {
                $(that).removeClass('disabled');
                btnReset.removeClass('disabled');
                setCookie('register_response', '');
                $('#sppiner-loading').hide();
                clearInterval(intervalInit);
            }
        }, 1000);
    });


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

    function __setLoadLocalStorage() {
        const substation = $('#substation');
        const levelTension = $('#level-tension');
        const measurementPoint = $('#measurement-point');

        if (substation.val() !== null) {
            localStorage.setItem('substation', $('[id="substation_hidden"]').val());
        }

        if (levelTension.val() !== null) {
            localStorage.setItem('level_tension', $('[id="level_tension_hidden"]').val());

        }

        if (measurementPoint.val() !== null) {
            localStorage.setItem('measurement_point', $('[id="measurement_point_hidden"]').val());
        }
        __getTrackingSelected();
        __getPointReload();
    }


    function __getLoadLocalStorage() {
        let idclient = localStorage.getItem('idclient');
        const substation = localStorage.getItem('substation');
        const levelTension = localStorage.getItem('level_tension');
        const measurementPoint = localStorage.getItem('measurement_point');

        const month = localStorage.getItem('month');
        const hrOrMin = localStorage.getItem('hr_or_min');
        const typeFile = localStorage.getItem('type_file');

        if (month !== null) {
            $('#months').val(month).formSelect();
        }

        if (hrOrMin !== null) {
            $('[name="hr_or_min"][value="' + hrOrMin + '"]').attr('checked', true)
        }

        if (typeFile !== null) {
            $('[name="type_file"][value="' + typeFile + '"]').attr('checked', true)
        }

        if (idclient === null) {
            idclient = $('[id="client"]').val();
        }

        $('#sppiner-loading').show();
        $('#client').val(idclient).formSelect();
        __getSubstation({
            'idclient': idclient
        });

        $('[id="substation_hidden"]').val(substation);
        $('[id="level_tension_hidden"]').val(levelTension);
        $('[id="measurement_point_hidden"]').val(measurementPoint);
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

    function __getPointReload() {
        const measurementPoint = $('#measurement-point');
        let totalPoints = measurementPoint.find('option:not([value="__all__"])').length;
        const optionSelected = measurementPoint.find('option:not([value="__all__"]):selected').length;
        if (optionSelected > 0) {
            totalPoints = optionSelected;
        }
        $('[id="points-cn"]').val(totalPoints);
    }

    setTimeout(function () {
        __getTrackingSelected();
    }, 500);
}(jQuery, window, document));