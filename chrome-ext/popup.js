/** Base URL for the Resume Couturier API (same origin as FastAPI). */
const API_BASE = 'http://127.0.0.1:8000';
const PARSED_RESUME_STORAGE_KEY = 'parsedResumeText';
const CAPTURED_JOB_DESCRIPTION_KEY = 'capturedJobDescription';
const GEMINI_MODEL_STORAGE_KEY = 'geminiModel';
const GEMINI_MODEL_OPTIONS = [
  'gemini-3.1-pro-preview',
  'gemini-3-flash-preview',
  'gemini-3.1-flash-lite-preview',
  'gemini-2.5-pro',
  'gemini-2.5-flash',
  'gemini-2.5-flash-lite',
];
const DEFAULT_GEMINI_MODEL = 'gemini-2.5-flash';

const JOB_DESCRIPTION_HOST_MAP = {
  'linkedin.com': [
    { identifier: 'componentKey', valuePattern: '^JobDetails_AboutTheJob_\\d+$' },
    { tag: 'div', classes: ['description__text', 'description__text--rich'] }
  ],
  'glassdoor.com': [{ tag: 'div', classes: ['JobDetails_jobDescription__uW_fK'] }],
};

function normalizeJobPortalHost(hostname) {
  const h = hostname.toLowerCase();
  if (h === 'linkedin.com' || h.endsWith('.linkedin.com')) {
    return 'linkedin.com';
  }
  if (h === 'glassdoor.com' || h.endsWith('.glassdoor.com')) {
    return 'glassdoor.com';
  }
  return null;
}

function extractJobDescriptionInPage(selectorList) {
  for (const spec of selectorList) {
    if (spec.identifier && spec.valuePattern) {
      const regex = new RegExp(spec.valuePattern);
      const nodes = document.getElementsByTagName(spec.tag || '*');
      for (let i = 0; i < nodes.length; i++) {
        const el = nodes[i];
        let val = el.getAttribute(spec.identifier);
        if (val == null && spec.identifier in el) {
          val = el[spec.identifier];
        }
        if (typeof val === 'string' && regex.test(val)) {
          return {
            ok: true,
            html: el.innerHTML,
            text: (el.innerText || '').trim(),
          };
        }
      }
    } else {
      const tag = spec.tag || 'div';
      const required = spec.classes || [];
      const nodes = document.getElementsByTagName(tag);
      for (let i = 0; i < nodes.length; i++) {
        const el = nodes[i];
        const cl = el.classList;
        let all = true;
        for (let j = 0; j < required.length; j++) {
          if (!cl.contains(required[j])) {
            all = false;
            break;
          }
        }
        if (all) {
          return {
            ok: true,
            html: el.innerHTML,
            text: (el.innerText || '').trim(),
          };
        }
      }
    }
  }
  return { ok: false, html: '', text: '' };
}

function queryActiveTab() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs?.[0] || null);
    });
  });
}


function getStoredCapturedJobDescription() {
  return new Promise((resolve) => {
    chrome.storage.local.get([CAPTURED_JOB_DESCRIPTION_KEY], (result) => {
      if (chrome.runtime.lastError) {
        console.error('storage.get job desc:', chrome.runtime.lastError.message);
        resolve(null);
        return;
      }
      resolve(result[CAPTURED_JOB_DESCRIPTION_KEY] || null);
    });
  });
}

function saveCapturedJobDescription(record) {
  return new Promise((resolve) => {
    chrome.storage.local.set({ [CAPTURED_JOB_DESCRIPTION_KEY]: record }, resolve);
  });
}

const authSection = document.getElementById('authSection');
const mainSection = document.getElementById('mainSection');
const loginBtn = document.getElementById('loginBtn');
const authError = document.getElementById('authError');
const userLine = document.getElementById('userLine');

const uploadSection = document.getElementById('uploadSection');
const resumeFileInput = document.getElementById('resumeFileInput');
const parseBtn = document.getElementById('parseBtn');
const parseStatus = document.getElementById('parseStatus');

const templateSection = document.getElementById('templateSection');
const jobDescriptionContainer = document.getElementById('jobDescriptionContainer');
const jobDescriptionText = document.getElementById('jobDescriptionText');
const jdStatus = document.getElementById('jdStatus');
const templatesStatus = document.getElementById('templatesStatus');
const templatesList = document.getElementById('templatesList');
const tailorBtn = document.getElementById('tailorBtn');
const backToUploadBtn = document.getElementById('backToUploadBtn');
const geminiModelSelect = document.getElementById('geminiModelSelect');
const generationStatus = document.getElementById('generationStatus');
const resultSection = document.getElementById('resultSection');
const previewPdfBtn = document.getElementById('previewPdfBtn');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');
const keywordsTags = document.getElementById('keywordsTags');

/** @type {string | null} */
let selectedTemplateId = null;
/** @type {string | null} */
let authToken = null;
/** @type {string | null} */
let generatedPdfUrl = null;
let selectedGeminiModel = DEFAULT_GEMINI_MODEL;

function showAuthView() {
  authSection.classList.add('visible');
  mainSection.classList.remove('visible');
}

function showMainView() {
  authSection.classList.remove('visible');
  mainSection.classList.add('visible');
}

function showUploadSection() {
  uploadSection.classList.add('visible');
  templateSection.classList.remove('visible');
}

function showTemplateSection() {
  uploadSection.classList.remove('visible');
  templateSection.classList.add('visible');
}

function setParseStatus(message, isError) {
  parseStatus.textContent = message;
  parseStatus.style.color = isError ? '#c5221f' : '#666';
}

function setGenerationStatus(message, isError) {
  generationStatus.textContent = message;
  generationStatus.style.color = isError ? '#c5221f' : '#666';
}

function getStoredParsedText() {
  return new Promise((resolve) => {
    chrome.storage.local.get([PARSED_RESUME_STORAGE_KEY], (result) => {
      if (chrome.runtime.lastError) {
        console.error('storage.get error:', chrome.runtime.lastError.message);
        resolve(null);
        return;
      }
      resolve(result[PARSED_RESUME_STORAGE_KEY] || null);
    });
  });
}

function saveParsedText(parsedText) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.set({ [PARSED_RESUME_STORAGE_KEY]: parsedText }, () => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve();
    });
  });
}

function getStoredGeminiModel() {
  return new Promise((resolve) => {
    chrome.storage.local.get([GEMINI_MODEL_STORAGE_KEY], (result) => {
      if (chrome.runtime.lastError) {
        console.error('storage.get error:', chrome.runtime.lastError.message);
        resolve(DEFAULT_GEMINI_MODEL);
        return;
      }
      const stored = result[GEMINI_MODEL_STORAGE_KEY];
      if (stored && GEMINI_MODEL_OPTIONS.includes(stored)) {
        resolve(stored);
        return;
      }
      resolve(DEFAULT_GEMINI_MODEL);
    });
  });
}

function saveGeminiModel(model) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.set({ [GEMINI_MODEL_STORAGE_KEY]: model }, () => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      resolve();
    });
  });
}

function clearGeneratedResult() {
  if (generatedPdfUrl) {
    URL.revokeObjectURL(generatedPdfUrl);
    generatedPdfUrl = null;
  }
  resultSection.classList.remove('visible');
  keywordsTags.innerHTML = '';
  setGenerationStatus('', false);
}

function renderMissingKeywords(missingKeywordsRaw) {
  keywordsTags.innerHTML = '';
  const keywords = (missingKeywordsRaw || '')
    .split(',')
    .map((k) => k.trim())
    .filter(Boolean);

  if (keywords.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'muted small';
    empty.textContent = 'No missing keywords reported.';
    keywordsTags.appendChild(empty);
    return;
  }

  keywords.forEach((keyword) => {
    const tag = document.createElement('span');
    tag.className = 'keyword-tag';
    tag.textContent = keyword;
    keywordsTags.appendChild(tag);
  });
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
  clearGeneratedResult();

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

async function parseResumeFile(file) {
  if (!authToken) {
    throw new Error('Missing auth token. Please sign in again.');
  }

  const formData = new FormData();
  formData.append('file', file, file.name);

  const response = await fetch(`${API_BASE}/resume/parse`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
    body: formData,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const detail = payload?.detail || `HTTP ${response.status}`;
    throw new Error(detail);
  }

  return payload?.parsed_text || payload?.markdown || '';
}

async function generateResume(templateId, parsedResumeText, geminiModel, jobDesc) {
  if (!authToken) {
    throw new Error('Missing auth token. Please sign in again.');
  }

  const response = await fetch(`${API_BASE}/resume/generate/${templateId}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_info: parsedResumeText,
      job_desc: jobDesc || '',
      custom_instructions: '',
      gemini_model: geminiModel,
    }),
  });

  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const payload = await response.json();
      if (payload?.detail) detail = payload.detail;
    } catch {
      // response body may not be JSON
    }
    throw new Error(detail);
  }

  const missingKeywords = response.headers.get('x-ats-missing-keywords') || '';
  const pdfBlob = await response.blob();
  return { missingKeywords, pdfBlob };
}

async function runLiveJDCheck() {
  if (jdStatus) {
    jdStatus.innerHTML = '<span style="color: #1a73e8;">Checking for JD...</span>';
  }

  try {
    const tab = await queryActiveTab();
    if (!tab || !tab.id || !tab.url) {
      if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
      return;
    }

    const hostname = new URL(tab.url).hostname;
    const portalHost = normalizeJobPortalHost(hostname);
    if (!portalHost || !JOB_DESCRIPTION_HOST_MAP[portalHost]) {
      if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
      return;
    }

    const injected = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractJobDescriptionInPage,
      args: [JOB_DESCRIPTION_HOST_MAP[portalHost]],
    });

    const result = injected?.[0]?.result;
    if (result && result.ok && result.text) {
      const record = {
        portal: portalHost,
        sourceUrl: tab.url,
        html: result.html,
        text: result.text,
        capturedAt: Date.now(),
      };
      await saveCapturedJobDescription(record);
      if (jobDescriptionText) jobDescriptionText.value = record.text;
      if (jdStatus) jdStatus.innerHTML = '<span style="color: #0f9d58;">Updated JD!</span>';
    } else {
      if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
    }
  } catch (err) {
    console.warn('Live JD check failed:', err);
    if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
  }
}

async function startPostLoginFlow() {
  const jd = await getStoredCapturedJobDescription();
  if (jd && jd.text) {
    jobDescriptionText.value = jd.text;
  } else {
    jobDescriptionText.value = '';
  }

  // Attempt live extraction exactly when transitioning to template layout
  runLiveJDCheck();

  const existingParsedText = await getStoredParsedText();
  if (existingParsedText) {
    showTemplateSection();
    loadLatexTemplates();
    return;
  }

  showUploadSection();
  templatesList.innerHTML = '';
  setTemplatesStatus('', false);
}

function afterLogin(token) {
  authToken = token;
  authError.textContent = '';
  setParseStatus('', false);
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

  getStoredGeminiModel()
    .then((model) => {
      selectedGeminiModel = model;
      if (geminiModelSelect) geminiModelSelect.value = model;
      return startPostLoginFlow();
    })
    .catch((err) => {
      console.error('post-login flow:', err);
      showUploadSection();
      setParseStatus('Could not read local cache.', true);
    });
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

parseBtn.addEventListener('click', async () => {
  const file = resumeFileInput.files?.[0];
  if (!file) {
    setParseStatus('Please choose a PDF or DOCX file first.', true);
    return;
  }

  parseBtn.disabled = true;
  setParseStatus('Parsing resume…', false);

  try {
    const parsedText = await parseResumeFile(file);
    if (!parsedText) {
      throw new Error('No parsed_text returned by API.');
    }
    await saveParsedText(parsedText);
    setParseStatus('Resume parsed and saved locally.', false);
    showTemplateSection();
    loadLatexTemplates();
  } catch (err) {
    console.error('parse resume:', err);
    setParseStatus(err.message || 'Failed to parse resume.', true);
  } finally {
    parseBtn.disabled = false;
  }
});

backToUploadBtn.addEventListener('click', () => {
  clearGeneratedResult();
  setTemplatesStatus('', false);
  templatesList.innerHTML = '';
  selectedTemplateId = null;
  tailorBtn.disabled = true;
  showUploadSection();
  setParseStatus('', false);
});

geminiModelSelect.addEventListener('change', () => {
  const model = geminiModelSelect.value;
  if (!GEMINI_MODEL_OPTIONS.includes(model)) {
    return;
  }
  selectedGeminiModel = model;
  saveGeminiModel(model).catch((err) => {
    console.error('save gemini model:', err);
    setGenerationStatus('Could not persist selected model.', true);
  });
});

tailorBtn.addEventListener('click', () => {
  if (!selectedTemplateId) {
    setGenerationStatus('Please select a template first.', true);
    return;
  }

  tailorBtn.disabled = true;
  clearGeneratedResult();
  setGenerationStatus('Generating resume…', false);

    getStoredParsedText()
    .then(async (parsedText) => {
      if (!parsedText) {
        throw new Error('No parsed resume found. Please upload and parse again.');
      }

      const jobDesc = jobDescriptionText.value.trim();

      const { missingKeywords, pdfBlob } = await generateResume(
        selectedTemplateId,
        parsedText,
        selectedGeminiModel,
        jobDesc,
      );
      if (generatedPdfUrl) URL.revokeObjectURL(generatedPdfUrl);
      generatedPdfUrl = URL.createObjectURL(pdfBlob);

      previewPdfBtn.onclick = () => {
        openThumbnailInNewTab(generatedPdfUrl);
      };

      downloadPdfBtn.onclick = () => {
        const anchor = document.createElement('a');
        anchor.href = generatedPdfUrl;
        anchor.download = `tailored-resume-template-${selectedTemplateId}.pdf`;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
      };

      renderMissingKeywords(missingKeywords);
      resultSection.classList.add('visible');
      setGenerationStatus('Resume generated successfully.', false);
    })
    .catch((err) => {
      console.error('generate resume:', err);
      setGenerationStatus(err.message || 'Failed to generate resume.', true);
    })
    .finally(() => {
      tailorBtn.disabled = false;
    });
});

chrome.identity.getAuthToken({ interactive: false }, (token) => {
  if (chrome.runtime.lastError || !token) {
    showAuthView();
    return;
  }
  afterLogin(token);
});

// Setup live listeners so side panel updates automatically without reopening
if (chrome.tabs) {
  chrome.tabs.onActivated.addListener(() => {
    // Only run if the template section is visible (where jd status lives)
    if (templateSection && templateSection.classList.contains('visible')) {
      runLiveJDCheck();
    }
  });

  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if ((changeInfo.status === 'complete' || changeInfo.url) &&
        templateSection && templateSection.classList.contains('visible') &&
        tab.active) {
      runLiveJDCheck();
    }
  });
}

if (chrome.storage) {
  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === 'local' && changes[CAPTURED_JOB_DESCRIPTION_KEY]) {
      const newValue = changes[CAPTURED_JOB_DESCRIPTION_KEY].newValue;
      if (newValue && newValue.text && templateSection && templateSection.classList.contains('visible')) {
        if (jobDescriptionText) jobDescriptionText.value = newValue.text;
        if (jdStatus) jdStatus.innerHTML = '<span style="color: #0f9d58;">Updated JD! (from active tab)</span>';
      }
    }
  });
}
