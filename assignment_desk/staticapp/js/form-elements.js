import $ from 'jquery';
import {
  ripple,
  select
} from 'immaterial-ui';

$(document).ready(() => {
  window.selectBoxes = $('select.select').map(select.build);
});
