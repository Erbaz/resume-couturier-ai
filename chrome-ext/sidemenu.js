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
const additionalInstructionsText = document.getElementById('additionalInstructionsText');
const customTemplateText = document.getElementById('customTemplateText');
const customTemplateFile = document.getElementById('customTemplateFile');
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

function validateTailorBtn() {
  const hasBaseTemplate = selectedTemplateId !== null;
  const hasCustomLatex = customTemplateText && customTemplateText.value.trim().length > 0;
  const hasCustomFile = customTemplateFile && customTemplateFile.files && customTemplateFile.files.length > 0;
  tailorBtn.disabled = !(hasBaseTemplate || hasCustomLatex || hasCustomFile);
}

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

if (customTemplateText) {
  customTemplateText.addEventListener('input', () => {
    if (customTemplateText.value.trim().length > 0) {
      selectedTemplateId = null;
      templatesList.querySelectorAll('.template-card').forEach(el => el.classList.remove('selected'));
    }
    validateTailorBtn();
  });
}

if (customTemplateFile) {
  customTemplateFile.addEventListener('change', () => {
    if (customTemplateFile.files && customTemplateFile.files.length > 0) {
      selectedTemplateId = null;
      templatesList.querySelectorAll('.template-card').forEach(el => el.classList.remove('selected'));
    }
    validateTailorBtn();
  });
}

async function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

tailorBtn.addEventListener('click', () => {
  const hasSelected = !!selectedTemplateId;
  const hasPaste = customTemplateText && customTemplateText.value.trim();
  const hasFile = customTemplateFile && customTemplateFile.files && customTemplateFile.files.length > 0;

  if (!hasSelected && !hasPaste && !hasFile) {
    setGenerationStatus('Please select a template or provide your own LaTeX code.', true);
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
      const customInst = additionalInstructionsText ? additionalInstructionsText.value.trim() : '';

      let templateLatex = customTemplateText ? customTemplateText.value.trim() : '';
      if (hasFile) {
        try {
          templateLatex = await readFileAsText(customTemplateFile.files[0]);
        } catch (err) {
          console.error('read template file:', err);
          throw new Error('Failed to read uploaded template file.');
        }
      }

      const { missingKeywords, pdfBlob } = await generateResume(
        selectedTemplateId,
        parsedText,
        selectedGeminiModel,
        jobDesc,
        customInst,
        templateLatex
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
    if (templateSection && templateSection.classList.contains('visible')) {
      runLiveJDCheck();
    }
  });

  let updateTimeout;
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if ((changeInfo.status === 'complete' || changeInfo.url) &&
        templateSection && templateSection.classList.contains('visible') &&
        tab.active) {
      
      // Debounce slightly to allow the DOM to start rendering in SPAs
      clearTimeout(updateTimeout);
      updateTimeout = setTimeout(() => {
        runLiveJDCheck();
      }, 500);
    }
  });

  // Specifically catch SPA history changes (like clicking a new job in a list)
  chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    if (templateSection && templateSection.classList.contains('visible') && details.tabId !== -1) {
      clearTimeout(updateTimeout);
      updateTimeout = setTimeout(() => {
        runLiveJDCheck();
      }, 500);
    }
  });
}

// React to DOM changes reported by content script
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'JD_EXTRACTED' && message.record) {
    if (templateSection && templateSection.classList.contains('visible')) {
      if (jobDescriptionText) jobDescriptionText.value = message.record.text;
      if (jdStatus) jdStatus.innerHTML = '<span style="color: #0f9d58;">Updated JD! (detected change)</span>';
    }
  }
});

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
