'use strict';
// Native dialog handles keyboard focus, Escape and the modal backdrop.
const opener = document.querySelector('button[data-modal]');
const dialog = document.querySelector('dialog');
if (opener && dialog) {
  opener.addEventListener('click', () => {
    dialog.showModal();
    opener.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('menu-open');
  });
  dialog.querySelector('[data-action="modal-close"]').addEventListener('click', () => dialog.close());
  dialog.querySelectorAll('a').forEach(link => link.addEventListener('click', () => dialog.close()));
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    opener.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('menu-open');
  });
}
