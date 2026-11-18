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
  const card = form.closest('.form-card');
  const heading = card ? card.querySelector('.form-heading') : null;
  const successBox = card ? card.querySelector('[data-form-success]') : null;
  const endpoint = form.dataset.endpoint || '';
  const realEndpoint = /^https:\/\/formspree\.io\/f\/[a-zA-Z0-9]+$/.test(endpoint);
  const defaultLabel = button.innerHTML;
  const TIMEOUT_MS = 20000;
  // Sperren gegen Mehrfachversand: submitting = Anfrage läuft, sent = bereits erfolgreich gesendet.
  let submitting = false;
  let sent = false;

  const setStatus = (message, state) => {
    status.textContent = message;
    status.dataset.state = state || '';
  };
  const setBusy = busy => {
    button.disabled = busy;
    button.classList.toggle('is-loading', busy);
    if (busy) {
      button.setAttribute('aria-busy', 'true');
      button.textContent = form.dataset.msgSending;
    } else {
      button.removeAttribute('aria-busy');
      button.innerHTML = defaultLabel;
    }
    form.classList.toggle('is-submitting', busy);
    form.querySelectorAll('input, select, textarea').forEach(field => { field.disabled = busy; });
  };
  const showSuccess = () => {
    sent = true;
    form.reset();
    form.hidden = true;
    if (heading) heading.hidden = true;
    if (successBox) {
      successBox.hidden = false;
      successBox.focus({ preventScroll: true });
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      successBox.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
    } else {
      setStatus(form.dataset.msgSuccess, 'success');
    }
  };

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (submitting || sent) return;
    if (!form.reportValidity()) return;
    if (!realEndpoint) {
      setStatus(form.dataset.msgUnconfigured, 'error');
      return;
    }
    if (form.querySelector('[name="_gotcha"]').value.trim()) return;
    // Daten vor dem Sperren der Felder einlesen (gesperrte Felder werden nicht übertragen).
    const payload = new FormData(form);
    submitting = true;
    setStatus(form.dataset.msgSending, 'sending');
    setBusy(true);
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), TIMEOUT_MS);
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: payload,
        headers: { Accept: 'application/json' },
        signal: controller.signal
      });
      if (!response.ok) {
        throw new Error(`Submission failed (${response.status})`);
      }
      setStatus('', '');
      showSuccess();
    } catch (error) {
      // Do not expose potentially sensitive submission contents in logs.
      setBusy(false);
      setStatus(form.dataset.msgError, 'error');
    } finally {
      window.clearTimeout(timer);
      submitting = false;
    }
  });
})();
