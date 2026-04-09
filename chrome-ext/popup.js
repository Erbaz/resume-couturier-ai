/** Base URL for the Resume Couturier API (same origin as FastAPI). */
const API_BASE = 'http://127.0.0.1:8000';

const authSection = document.getElementById('authSection');
const mainSection = document.getElementById('mainSection');
const loginBtn = document.getElementById('loginBtn');
const authError = document.getElementById('authError');
const userLine = document.getElementById('userLine');
const templatesStatus = document.getElementById('templatesStatus');
const templatesList = document.getElementById('templatesList');
const tailorBtn = document.getElementById('tailorBtn');

/** @type {string | null} */
let selectedTemplateId = null;

function showAuthView() {
  authSection.classList.add('visible');
  mainSection.classList.remove('visible');
}

function showMainView() {
  authSection.classList.remove('visible');
  mainSection.classList.add('visible');
}

/**
 * @param {string} thumbnail
 * @returns {string}
 */
function resolveThumbnailUrl(thumbnail) {
  if (!thumbnail) return '';
  if (/^https?:\/\//i.test(thumbnail)) return thumbnail;
  const name = thumbnail.replace(/^.*[/\\]/, '');
  return `${API_BASE}/assets/${name}`;
}

/** Opens image URL in a new browser tab (does not change template selection). */
function openThumbnailInNewTab(url) {
  if (!url) return;
  if (chrome.tabs?.create) {
    chrome.tabs.create({ url });
  } else {
    window.open(url, '_blank', 'noopener,noreferrer');
  }
}

function setTemplatesStatus(message, isError) {
  templatesStatus.textContent = message;
  templatesStatus.style.color = isError ? '#c5221f' : '#666';
}

function renderTemplateList(templates) {
  templatesList.innerHTML = '';
  selectedTemplateId = null;
  tailorBtn.disabled = true;

  templates.forEach((t) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'template-card';
    card.dataset.templateId = t.id;

    const thumbUrl = resolveThumbnailUrl(t.thumbnail);

    const onThumbClick = (e) => {
      e.stopPropagation();
      openThumbnailInNewTab(thumbUrl);
    };

    const img = document.createElement('img');
    img.alt = '';
    img.loading = 'lazy';
    if (thumbUrl) {
      img.src = thumbUrl;
      img.title = 'Open preview in new tab';
      img.addEventListener('click', onThumbClick);
    }
    img.addEventListener('error', () => {
      const fallback = Object.assign(document.createElement('div'), {
        className: 'template-thumb-fallback',
        textContent: 'No preview',
      });
      if (thumbUrl) {
        fallback.title = 'Open preview in new tab';
        fallback.classList.add('template-thumb-fallback--clickable');
        fallback.addEventListener('click', onThumbClick);
      }
      img.replaceWith(fallback);
    });

    const nameEl = document.createElement('div');
    nameEl.className = 'template-name';
    nameEl.textContent = t.name || `Template ${t.id}`;

    card.appendChild(img);
    card.appendChild(nameEl);

    card.addEventListener('click', () => {
      selectedTemplateId = t.id;
      tailorBtn.disabled = false;
      templatesList.querySelectorAll('.template-card').forEach((el) => {
        el.classList.toggle('selected', el.dataset.templateId === String(t.id));
      });
    });

    templatesList.appendChild(card);
  });
}

function loadLatexTemplates() {
  setTemplatesStatus('Loading templates…', false);
  templatesList.innerHTML = '';

  fetch(`${API_BASE}/resume/latex-templates`)
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        setTemplatesStatus('No templates available.', false);
        tailorBtn.disabled = true;
        return;
      }
      setTemplatesStatus('', false);
      renderTemplateList(data);
    })
    .catch((err) => {
      console.error('latex-templates:', err);
      tailorBtn.disabled = true;
      setTemplatesStatus('Could not load templates. Is the API running?', true);
    });
}

function afterLogin(token) {
  authError.textContent = '';
  showMainView();

  fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
    headers: { Authorization: 'Bearer ' + token },
  })
    .then((r) => r.json())
    .then((data) => {
      userLine.textContent = data.email ? `Signed in as ${data.email}` : 'Signed in';
    })
    .catch(() => {
      userLine.textContent = 'Signed in';
    });

  loadLatexTemplates();
}

function requestLogin(interactive) {
  chrome.identity.getAuthToken({ interactive }, (token) => {
    if (chrome.runtime.lastError) {
      console.error('Auth Error:', chrome.runtime.lastError.message);
      authError.textContent = chrome.runtime.lastError.message;
      return;
    }
    afterLogin(token);
  });
}

loginBtn.addEventListener('click', () => requestLogin(true));

tailorBtn.addEventListener('click', () => {
  console.log('Tailor Resume (placeholder)', { selectedTemplateId });
});

chrome.identity.getAuthToken({ interactive: false }, (token) => {
  if (chrome.runtime.lastError || !token) {
    showAuthView();
    return;
  }
  afterLogin(token);
});
