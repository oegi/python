$(function () {
    'use strict';

    $('.jstree-cls').each((k, ele) => {
        $.ajax({
            'async': true,
            'crossDomain': true,
            'url': '/api/tree/',
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            'data': JSON.stringify({
                'path': $(ele).data('path')
            }),
        }).done(function (response, status) {
            var data = response.data;
            if (data.length !== 0) {

                $('#' + $(ele).attr('id') + '').jstree({
                    'core': {
                        'data': data
                    },
                    'plugins': ['sort', 'types']
                }).bind('select_node.jstree', function (e, data) {
                    $('#' + $(ele).attr('id') + '').jstree('save_state');
                }).on('activate_node.jstree', function (e, data) {
                    const node = data.node;
                    const href = node.data.href;
                    if (typeof href !== 'undefined')
                        window.location.href = href;
                });
            }
        });
    });
}());

