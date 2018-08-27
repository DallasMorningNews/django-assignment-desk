// import MaterialDateTimePicker from 'material-datetime-picker';
// import MaterialDatePicker from '../../../common/material-datepicker';
// import moment from 'moment';
import Pikaday from 'pikaday';

const inputField = document.getElementById('id_beginning_date');

const picker = new Pikaday({
  field: inputField,
  format: 'YYYY-MM-DD',
  reposition: false,
  firstDay: 1,
  // pickWholeWeek: true,
  // onSelect: function (date) {
  //   var mondayDate = date.getDate() - (date.getDay() - 1);
  //   var monday = new Date(date.setDate(mondayDate));
  //   var sunday = new Date(date.setDate(mondayDate + 6));
  //   inputField.value = monday.toLocaleDateString();
  // }
});

window.pkr = picker;

// const datePicker = new MaterialDatePicker({
//   {
//     name: 'Week only',
//     format: ['[Week of] MMM D, YYYY'],
//     priority: 2,
//     rounding: 'week',
//     roundTo: 'start',
//   },
//   mode: value,
//   boundField: ui.pubDateField,
//   overlayParent: document.body,
//   onChangeEvent: 'changeDate',
// });

// input.addEventListener('focus', () => datePicker.picker.show());
// input.addEventListener('blur', () => datePicker.picker.hide());

