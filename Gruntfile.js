module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        bowercopy: {
            options: {
                clean: true
                //srcPrefix: 'bower_components'
            },
            libs: {
                options: {
                    destPrefix: 'appcore/static'
                },
                files: {
                    'libs/jq/': 'jquery/dist/*',
                    'libs/jq-confirm2': 'jquery-confirm2/dist/*',
                    'libs/mt': 'materialize/dist/*',
                    'libs/fontaw/css': 'fontawesome/css/*',
                    'libs/fontaw/js': 'fontawesome/js/*',
                    'libs/fontaw/webfonts': 'fontawesome/webfonts/*',
                    'libs/material-design-lite/css': 'material-design-lite/material.*.css',
                    'libs/material-design-lite/js': 'material-design-lite/material.*.js',
                    'libs/bts-mt-datetm/css': 'bootstrap-material-datetimepicker/css/*',
                    'libs/bts-mt-datetm/js': 'bootstrap-material-datetimepicker/js/*',
                    'libs/bts-mt-datetm/font': 'bootstrap-material-datetimepicker/font/*',
                    'libs/bootstrap': 'bootstrap/dist/*',
                    'libs/popper': 'popper.js/dist/*',
                    'libs/jstree': 'jstree/dist/*',
                    'libs/moment': 'moment/min/*',
                    'libs/jquery-validation': 'jquery-validation/dist/*',
                    'libs/dt/css': 'datatables/media/css/*',
                    'libs/dt/images': 'datatables/media/images/*',
                    'libs/dt/translations': 'datatables.net-translations/locale/*',
                    'libs/dt/js': 'datatables/media/js/*',
                }
            }
        },
        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'node_modules/material-design-icons',
                        src: ['iconfont/*'],
                        dest: 'appcore/static/libs/mt-design-icons',
                        filter: 'isFile'
                    },
                ],
            },
        },
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-bowercopy');
    // Default grunt copy
    grunt.loadNpmTasks('grunt-contrib-copy');
    // Default task(s).
    grunt.registerTask('default', ['bowercopy', 'copy']);
};