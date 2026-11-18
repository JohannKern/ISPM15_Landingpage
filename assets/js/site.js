/* Lightweight progressive enhancement. No cookies, analytics or external JS packages. */
(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (menu && nav) {
    const closeMenu = () => {
      nav.classList.remove('is-open');
      menu.setAttribute('aria-expanded', 'false');
    };
    menu.addEventListener('click', () => {
      const open = !nav.classList.contains('is-open');
      nav.classList.toggle('is-open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeMenu();
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 880) closeMenu();
    });
  }

  const form = document.querySelector('[data-demo-form]');
  if (!form) return;
  const button = form.querySelector('[data-submit-button]');
  const status = form.querySelector('[data-form-status]');
  const endpoint = form.dataset.endpoint || '';
  const realEndpoint = /^https:\/\/formspree\.io\/f\/[a-zA-Z0-9]+$/.test(endpoint);
  const defaultLabel = button.innerHTML;

  const setStatus = (message, state) => {
    status.textContent = message;
    status.dataset.state = state || '';
  };
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    if (!realEndpoint) {
      setStatus(form.dataset.msgUnconfigured, 'error');
      return;
    }
    if (form.querySelector('[name="_gotcha"]').value.trim()) return;
    button.disabled = true;
    button.textContent = form.dataset.msgSending;
    setStatus('', '');
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) {
        throw new Error(`Submission failed (${response.status})`);
      }
      form.reset();
      setStatus(form.dataset.msgSuccess, 'success');
    } catch (error) {
      // Do not expose potentially sensitive submission contents in logs.
      setStatus(form.dataset.msgError, 'error');
    } finally {
      button.disabled = false;
      button.innerHTML = defaultLabel;
    }
  });
})();
