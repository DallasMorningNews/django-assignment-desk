import $ from 'jquery';
import { ripple } from 'immaterial-ui';


// $('.navbar .show-nav').bind('click', (e) => {
//   $(e.currentTarget).find('.header-burger').toggleClass('active');
//   $('.collapsible-nav').toggleClass('shown');
// });


// Initialize button ripples.
document.querySelectorAll('.btn')
  .forEach((el) => {
    ripple.Ripple.attachTo(el);
  });

document.querySelector('.navbar .show-nav')
  .addEventListener('click', (event) => {
    event.currentTarget.querySelector('.header-burger').classList.toggle('active');
    document.querySelector('.collapsible-nav').classList.toggle('shown');
  });


setTimeout(() => {
  document.querySelectorAll('.fab-delayed')
    .forEach((el) => {
      el.classList.remove('fab-exited');
    });
}, 280);

setTimeout(() => {
  document.querySelectorAll('.fab-delayed')
    .forEach((el) => {
      ripple.Ripple.attachTo(el);
    });
}, 480);
