/* Optional enhancements for the static pages. */
(() => {
  'use strict';

  function initializeNavigation() {
    const button = document.querySelector('.menu-toggle');
    const navigation = document.querySelector('#navigation');
    if (!button || !navigation) return;

    function setOpen(open) {
      navigation.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
    }

    button.addEventListener('click', () => {
      setOpen(button.getAttribute('aria-expanded') !== 'true');
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && navigation.classList.contains('open')) {
        setOpen(false);
        button.focus();
      }
    });

    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) setOpen(false);
    });

    window.matchMedia('(min-width: 801px)').addEventListener('change', event => {
      if (event.matches) setOpen(false);
    });
  }

  function initializeCertificateFilters() {
    const filters = document.querySelectorAll('[data-filter]');
    const certificates = document.querySelectorAll('.certificate');
    const counter = document.querySelector('#cert-count');
    if (!filters.length || !counter) return;

    filters.forEach(button => {
      button.addEventListener('click', () => {
        filters.forEach(filter => {
          const selected = filter === button;
          filter.classList.toggle('active', selected);
          filter.setAttribute('aria-pressed', String(selected));
        });

        let count = 0;
        certificates.forEach(certificate => {
          const visible = button.dataset.filter === 'All'
            || certificate.dataset.category === button.dataset.filter;
          certificate.hidden = !visible;
          if (visible) count++;
        });
        counter.textContent = `${count} CREDENTIAL${count === 1 ? '' : 'S'}`;
      });
    });
  }

  function initializeContact() {
    const emailLink = document.querySelector('.email-link');
    if (!emailLink) return;
    const email = emailLink.getAttribute('href').replace(/^mailto:/, '');
    const copyButton = document.querySelector('.copy-email');
    const copyStatus = document.querySelector('#copy-status');
    const form = document.querySelector('.contact-form');

    if (copyButton && copyStatus) {
      copyButton.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(email);
          copyStatus.textContent = 'Email address copied.';
        } catch {
          copyStatus.textContent = `Copy this address: ${email}`;
        }
      });
    }

    form?.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;

      const fields = new FormData(form);
      const value = name => String(fields.get(name) ?? '').trim();
      const subject = encodeURIComponent(value('subject'));
      const body = encodeURIComponent(
        `${value('message')}\n\nFrom: ${value('name')}\nReply to: ${value('email')}`
      );
      window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
      const status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Email draft requested. If your app did not open, use the email link or copy the address.';
      }
    });
  }

  function updateCopyrightYear() {
    const year = String(new Date().getFullYear());
    document.querySelectorAll('[data-year]').forEach(element => {
      element.textContent = year;
    });
  }

  initializeNavigation();
  initializeCertificateFilters();
  initializeContact();
  updateCopyrightYear();
})();
