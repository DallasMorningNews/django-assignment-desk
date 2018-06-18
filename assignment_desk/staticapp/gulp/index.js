'use strict';

const gulp = require('gulp');
const path = require('path');


module.exports = (tasks) => {
  tasks.forEach((name) => { gulp.task(name, require(`./tasks/${name}`)); });

  return gulp;
}
