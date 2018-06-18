'use strict';

const browserSync = require('browser-sync').create();
const fs = require('fs');
const os = require('os');
const runSequence = require('run-sequence');
const watch = require('gulp-watch');


const ssl = process.argv.indexOf('--ssl') !== -1;

const browserSyncConfig = {
  files: [
    './assignment_desk/**/static/**/*.{js,css}',
    './assignment_desk/**/templates/**/*.html',
  ],
  open: false,
  host: 'local-dev.dallasnews.com',
  proxy: {
    target: 'localhost:8000',
    middleware(req, res, next) {
      req.headers['X-Forwarded-Host'] = req.headers.host;
      req.headers['X-Forwarded-Proto'] = ssl ? 'https' : 'http';
      next();
    },
  },
  startPath: '/',
  ghostMode: false,
};


/**
 * If the below cert files are found, use them to configure our
 * local SSL server
 */
const key = `${os.homedir()}/.dmn-interactives/local-dev.dallasnews.com.key`;
const cert = `${os.homedir()}/.dmn-interactives/local-dev.dallasnews.com.crt`;

let useCerts = false;
try {
  fs.accessSync(key);
  fs.accessSync(cert);
  useCerts = true;
} catch (e) {
  // do nothing
}

if (useCerts && ssl) {
  browserSyncConfig.https = {
    key,
    cert,
  };
} else if (ssl) {
  /**
   * If no SSL certiricate is specified, but --ssl was passed, still enable
   * it but don't specify a local cert
   */
  browserSyncConfig.https = true;
}


module.exports = () => {
  browserSync.init(browserSyncConfig);
  watch('./assignment_desk/staticapp/scss/**/*.scss', () => { runSequence('scss'); });
};
