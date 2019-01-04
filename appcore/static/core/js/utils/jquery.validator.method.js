jQuery.validator.addMethod('extesion_file', function (value) {
    return (/\.(bmm)$/i).test(value);
}, 'Extensión de archivo incorrecta, por favor ingrese una extesion .bmm');


jQuery.validator.addMethod('filesize', function (value, element, arg) {
    const sizeFle = element.files[0].size;
    return (arg > sizeFle);
}, 'Ha superado el límite de 5MB del archivo');


jQuery.validator.addMethod('name_file', function (value, element, arg) {
    const nameFile = $(arg).val() + '.' + 'bmm';
    return (value === nameFile);
}, 'El nombre del archivo no es el mismo que el ID del medidor');

jQuery.validator.addMethod(
    'multiemails',
    function (value, element) {
        if (this.optional(element)) // return true on optional element
            return true;
        let valid = true;
        const emails = value.split(/[;,]+/); // split element by , and ;

        for (let i = 0; i < emails.length; i++) {
            value = emails[i];
            valid = valid && jQuery.validator.methods.email.call(this, $.trim(value), element);
        }

        return valid;
    },
    jQuery.validator.messages.email
);

jQuery.validator.addMethod('date_greater', function (value, element, params) {

    //let subStart = moment($(params[0]).val(), 'DD-MM-YYYY HH:mm');
    const subEnd = moment(value, 'DD-MM-YYYY HH:mm');
    const subNow = moment(moment(), 'DD-MM-YYYY HH:mm');

    if (!/Invalid|NaN/.test(subEnd) && !/Invalid|NaN/.test(subNow)) {
        if (subEnd.format('M') === subNow.format('M') && subEnd.format('D') === subNow.format('D')) {
            const monthStart = moment(subEnd.format('DD-MM-YYYY'), 'DD-MM-YYYY'),
                minStart = moment(subEnd.format('HH:mm'), 'HH:mm');
            const monthEnd = moment(subNow.format('DD-MM-YYYY'), 'DD-MM-YYYY'),
                minEnd = moment(subNow.format('HH:mm'), 'HH:mm');
            return (monthStart >= monthEnd && minStart <= minEnd);
        }
        return true;
    }
}, $.validator.format('No debe ser mayor a la fecha y hora actual.'));