import $ from 'jquery';
import Pikaday from 'pikaday';
import { select } from 'immaterial-ui';


$(document).ready(() => {
  window.selectBoxes = $('select.select').map(select.build);
});


const inputField = document.getElementById('id_beginning_date');


const picker = new Pikaday({
  field: inputField,
  format: 'YYYY-MM-DD',
  reposition: false,
  firstDay: 1,
});
