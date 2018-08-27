import Choices from 'choices.js';
import { ripple } from 'immaterial-ui';
import tingle from 'tingle.js';
import tippy from 'tippy.js';


import initializeMoment  from './moment-apstyle';


const allStaffers = [
  {
    value: '',
    label: 'Choose a staffer...',
    placeholder: true,
    active: false,
    customProperties: { firstName: '', lastName: '' },
  },
  ...stafferList,
];

const moment = initializeMoment();

const roleSlugNameCrosswalk = Array.from(document.querySelectorAll('td.role-name'))
  .map(el => [el.parentElement.getAttribute('data-role'), el.textContent])
  .reduce((o, current) => { o[current[0]] = current[1]; return o; }, {});

const modal = new tingle.modal({
  footer: true,
  stickyFooter: false,
  closeMethods: ['overlay', 'button', 'escape'],
  closeLabel: "Close",
  onOpen: () => {},
  onClose: () => { modal.modalBox.classList.add('ease-in'); },
  beforeClose: () => { return true; }
});

modal.modalBox.classList.add('ease-in');

const openAssignmentModal = (role, rawDate) => {
  const parsedDate = moment(rawDate);

  const targetElement = document.querySelector(`table tbody tr[data-role="${role}"] td[data-date="${rawDate}"]`);

  window.setTimeout(() => {
    modal.modalBox.classList.remove('ease-in');

    window.setTimeout(() => {
      modal.modal.querySelectorAll('.btn')
        .forEach((el) => {
          el.classList.add('shown');
          ripple.Ripple.attachTo(el);
        });
    }, 200);
  }, 300);

  const formPrefix = targetElement.getAttribute('data-prefix');
  const targetInputs = {
    staffer: targetElement.querySelector(`#id_${formPrefix}-staffer`),
    notes: targetElement.querySelector(`#id_${formPrefix}-notes`),
  };

  const initialValue = (targetInputs.staffer.value.length !== 0)
    ? stafferList.find(staffer => staffer.customProperties.id === parseInt(targetInputs.staffer.value, 10)).value
    : null;

  modal.setContent(`<div class="title-area"><div class="title-elements"><h3>Create assignment</h3><h5 class="role">${
    roleSlugNameCrosswalk[role]
  }</h5><h5 class="date">${
    parsedDate.format('dddd, MMM D, YYYY')
  }</h5></div></div>` +
  '<div class="assignment-modal-form">' +
    '<select id="modal-staffer"></select>' +
    '<div class="assignment-notes form-group">' +
    '    <textarea cols="40" rows="6" class="form-control" placeholder="Notes" title="" autocomplete="nope" id="id_assignment-notes">' +
        targetInputs.notes.value +
        '</textarea>' +
    '    <label class="control-label" for="id_assignment-notes">Notes</label>' +
    '    <i class="bar"></i>' +
    '    <div class="help-block"></div>' +
    '</div>' +
  `</div>`);

  const selectBox = new Choices(modal.modal.querySelector('#modal-staffer'), {
    addItems: true,
    sortFilter: (a, b) => {
      const firstNameA = a.customProperties.firstName || '';
      const firstNameB = b.customProperties.firstName || '';

      const lastNameA = a.customProperties.lastName || '';
      const lastNameB = b.customProperties.lastName || '';

      if (lastNameA.toLowerCase() !== lastNameB.toLowerCase()) {
        if (lastNameA.toLowerCase() < lastNameB.toLowerCase()) return -1;
        if (lastNameA.toLowerCase() > lastNameB.toLowerCase()) return 1;
      }

      if (firstNameA.toLowerCase() !== lastNameB.toLowerCase()) {
        if (firstNameA.toLowerCase() < lastNameB.toLowerCase()) return -1;
        if (firstNameA.toLowerCase() > lastNameB.toLowerCase()) return 1;
      }

      return 0;
    },
    // searchEnabled: true,
    // editItems: false,
    // duplicateItems: false,
    placeholderValue: 'This is a placeholder set in the config',
    searchPlaceholderValue: 'Search all staffers...',
    // searchFields: ['fullName', 'email'],
    choices: allStaffers,
    placeholder: true,
    maxItemCount: 1,
    position: 'bottom',

    callbackOnCreateTemplates: function (strToEl) {
      var classNames = this.config.classNames;
      var itemSelectText = this.config.itemSelectText;
      return {
        item: function (data) {
          const outerElClasses = [
            String(classNames.item),
            String(data.highlighted ? classNames.highlightedState : classNames.itemSelectable)
          ];

          const startingOuterTag = `<div class="${
            outerElClasses.join(' ')
          }" data-item data-id="${
            data.id
          }" data-value="${
            String(data.value)
          }" ${
            String(data.active ? 'aria-selected="true"' : '')
          } ${
            String(data.disabled ? 'aria-disabled="true"' : '')
          }>`;

          const endingOuterTag = '</div>';

          return (data.placeholder === true)
            ? strToEl([
              startingOuterTag,
              `<span class="staffer-placeholder">${
                String(data.label)
              }</span>`,
              endingOuterTag,
            ].join(' '))
            : strToEl([
              startingOuterTag,
              `<img class="staffer-mug" src="${
                (data.customProperties.imageURL === null)
                  ? String('')
                  : String(data.customProperties.imageURL)
              }" alt="${
                String(data.label)
              }" /><div class="staffer-details"><span class="staffer-name">${
                String(data.label)
              }</span><span class="staffer-email">${
                (data.customProperties.email === null)
                  ? String('(unknown email)')
                  : String(data.customProperties.email)
              }</span></div>`,
              endingOuterTag,
            ].join(' '));
        },
        choice: function (data) {
          const outerElClasses = [
            String(classNames.item),
            String(classNames.itemChoice),
            String(
              data.disabled
                ? classNames.itemDisabled
                : classNames.itemSelectable
            ),
          ];

          const startingOuterTag = `<div class="${
            outerElClasses.join(' ')
          }" data-select-text="${
            String(itemSelectText)
          }" data-choice ${
            String(
              data.disabled
                ? 'data-choice-disabled aria-disabled="true"'
                : 'data-choice-selectable'
            )
          } data-id="${
            String(data.id)
          }" data-value="${
            String(data.value)
          }" ${
            String(
              data.groupId > 0 ? 'role="treeitem"': 'role="option"'
            )
          }>`;
          const endingOuterTag = '</div>';

          return (data.placeholder === true)
            ? strToEl([
              startingOuterTag,
              `<span class="staffer-placeholder">${
                String(data.label)
              }</span>`,
              endingOuterTag,
            ].join(' '))
            : strToEl([
              startingOuterTag,
              `<img class="staffer-mug" src="${
                (data.customProperties.imageURL === null)
                  ? String('')
                  : String(data.customProperties.imageURL)
              }" alt="${
                String(data.label)
              }" /><div class="staffer-details"><span class="staffer-name">${
                String(data.label)
              }</span><span class="staffer-email">${
                (data.customProperties.email === null)
                  ? String('(unknown email)')
                  : String(data.customProperties.email)
              }</span></div>`,
              endingOuterTag,
            ].join(' '));
        },
      };
    }
  });

  if (initialValue !== null) {
    selectBox.setValueByChoice(initialValue);
  }

  modal.setFooterContent('');

  modal.addFooterBtn('OK', 'btn btn-default btn-primary-flat', function () {
    // Persist chosen staffer from modal to ModelForm.
    const userEnteredStafferID = (selectBox.getValue().value.length !== 0 )
      ? selectBox.getValue().customProperties.id
      : '';
    targetInputs.staffer.value = userEnteredStafferID;
    targetInputs.staffer.dispatchEvent(new Event('change'));

    // Persist notes from modal to ModelForm.
    const userEnteredNotes = modal.modalBox.querySelector('#id_assignment-notes').value;
    targetInputs.notes.value = userEnteredNotes;
    targetInputs.notes.dispatchEvent(new Event('change'));

    if (userEnteredStafferID !== '') {
      if (targetElement.classList.contains('empty')) targetElement.classList.remove('empty');
    } else {
      if (!targetElement.classList.contains('empty')) targetElement.classList.add('empty');
    }

    if (userEnteredNotes !== '') {
      if (!targetElement.classList.contains('has-notes')) targetElement.classList.add('has-notes');
    } else {
      if (targetElement.classList.contains('has-notes')) targetElement.classList.remove('has-notes');
    }

    modal.close();
  });

  // add another button
  modal.addFooterBtn('Cancel', 'btn btn-default btn-danger-flat', function () {
    // here goes some logic
    modal.close();
  });

  modal.open();
};


const assignmentCells = document.querySelectorAll('#assignment-forms tbody tr td:not(.role-name)');
const daySlugs = Array.from(document.querySelectorAll('#assignment-forms thead th:not(.spacer)'))
  .map(el => el.getAttribute('data-day'));


assignmentCells.forEach((cell, index) => {
  const parentRow = cell.parentElement;

  const cellAttributes = {
    day: cell.getAttribute('data-day'),
    date: cell.getAttribute('data-date'),
    prefix: cell.getAttribute('data-prefix'),
  };

  cell.addEventListener('click', () => {
    const roleSlug = parentRow.getAttribute('data-role');

    openAssignmentModal(roleSlug, cellAttributes.date);
  });

  const inputElements = {
    staffer: cell.querySelector(`.per-assignment-fields #id_${cellAttributes.prefix}-staffer`),
    notes: cell.querySelector(`.per-assignment-fields #id_${cellAttributes.prefix}-notes`),
  };

  inputElements.staffer.addEventListener('change', (event) => {
    const stafferImage = cell.querySelector('.staffer-info .staffer-image');
    const stafferName = cell.querySelector('.staffer-info .staffer-name');

    if (inputElements.staffer.value.length !== 0) {
      // Switch to the newly-selected staffer's information.
      const newStafferData = stafferList
        .find(staffer =>
          staffer.customProperties.id === parseInt(inputElements.staffer.value, 10)
      ).customProperties;

      stafferImage.setAttribute('src', newStafferData.imageURL);
      stafferImage.setAttribute('title', newStafferData.fullName);
      stafferImage.setAttribute('alt', newStafferData.fullName);

      stafferName.textContent = `${newStafferData.firstName[0]}. ${newStafferData.lastName}`;
    } else {
      // Clear all information describing the formerly selected staffer.
      stafferImage.setAttribute('src', '');
      stafferImage.setAttribute('alt', '');

      stafferName.textContent = '';
    }
  }, false);

  const notesTrigger = cell.querySelector('.notes-trigger');

  const notesTooltip = tippy.one(notesTrigger, {
    arrow: true,
    dynamicTitle: true,
    interactive: true,
    interactiveBorder: 3,
    placement: 'bottom',
    // flip: true,
    // flipBehavior: ['left', 'bottom'],
    trigger: 'manual',
  });

  notesTrigger.addEventListener('click', (event) => {
    event.stopPropagation();
    // console.log('NOTES TRIGGERED II.');

    notesTrigger.setAttribute('title', inputElements.notes.value);
    notesTooltip.show();

    // const stafferName = cell.querySelector('.staffer-info .staffer-name').textContent;
    // const dayFormatted = cell.getAttribute('data-day-formatted');

    // cell.setAttribute('data-staffer-name', stafferName);
    // cell.setAttribute('data-notes', `Notes for ${dayFormatted}: ${inputElements.notes.value}`);

    // cell.classList.add('notes-shown');

    // notesTrigger.querySelector('.close-notes').addEventListener('click', () => {
    //   event.stopPropagation();
    //   console.log('CLOSE NOTES.');
    // })
  });

  const copyForwardTrigger = cell.querySelector('.copy-to-subsequent-days');

  if (copyForwardTrigger !== null) {
    copyForwardTrigger.addEventListener('click', (event) => {
      event.stopPropagation();

      const slicedDays = daySlugs.slice(daySlugs.indexOf(cellAttributes.day) + 1);

      slicedDays.forEach((daySlug) => {
        const subsequentDayEl = parentRow.querySelector(`td[data-day="${daySlug}"`);

        if (subsequentDayEl.classList.contains('empty')) subsequentDayEl.classList.remove('empty');

        const subsequentPrefix = subsequentDayEl.getAttribute('data-prefix');

        const subsequentStafferInput = subsequentDayEl.querySelector(`.per-assignment-fields #id_${
          subsequentPrefix
        }-staffer`);

        subsequentStafferInput.value = inputElements.staffer.value;
        subsequentStafferInput.dispatchEvent(new Event('change'));
      });
    });
  } else {
    cell.querySelector('.cannot-copy-because-last').addEventListener('click', (event) => {
      event.stopPropagation();
    });
  }
});

document.querySelectorAll('.btn')
  .forEach((el) => { ripple.Ripple.attachTo(el); });
