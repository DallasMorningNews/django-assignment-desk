'use strict';

const gulp = require('./assignment_desk/staticapp/gulp')([
    'browserify',
    'scss',
    'server',
    'watchify'
]);


gulp.task('default', ['scss', 'watchify', 'server']);

gulp.task('build', ['scss', 'browserify']);
