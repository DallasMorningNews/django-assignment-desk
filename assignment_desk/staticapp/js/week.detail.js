import tippy from 'tippy.js';


const assignmentCells = document.querySelectorAll('.assignments-table tbody tr td:not(.role-name)');
const daySlugs = Array.from(document.querySelectorAll('#assignment-forms thead th:not(.spacer)'))
  .map(el => el.getAttribute('data-day'));


assignmentCells.forEach((cell, index) => {
  const notesTrigger = cell.querySelector('.notes-trigger');

  const notesTooltip = tippy.one(notesTrigger, {
    arrow: true,
    dynamicTitle: true,
    interactive: true,
    interactiveBorder: 3,
    placement: 'bottom',
    trigger: 'manual',
  });

  notesTrigger.addEventListener('click', (event) => {
    event.stopPropagation();
    notesTooltip.show();
  });
});
