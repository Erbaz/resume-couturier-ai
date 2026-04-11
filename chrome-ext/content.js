const CAPTURED_JOB_DESCRIPTION_KEY = 'capturedJobDescription';

const JOB_DESCRIPTION_HOST_MAP = {
  'linkedin.com': [
    { identifier: 'componentKey', valuePattern: '^JobDetails_AboutTheJob_\\d+$' },
    { tag: 'div', classes: ['description__text', 'description__text--rich'] },
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

let lastExtractedText = '';

function attemptExtraction() {
  const portalHost = normalizeJobPortalHost(window.location.hostname);
  if (!portalHost) return;

  const selectorList = JOB_DESCRIPTION_HOST_MAP[portalHost];
  if (!selectorList?.length) return;

  const result = extractJobDescriptionInPage(selectorList);
  if (result.ok && result.text && result.text !== lastExtractedText) {
    lastExtractedText = result.text;
    const record = {
      portal: portalHost,
      sourceUrl: window.location.href,
      html: result.html,
      text: result.text,
      capturedAt: Date.now(),
    };
    chrome.storage.local.set({ [CAPTURED_JOB_DESCRIPTION_KEY]: record }, () => {
      console.log('[Resume Couturier AI] Extracted and saved Job Description.');
      // Notify components like the side panel that JD has been updated via DOM change
      chrome.runtime.sendMessage({ type: 'JD_EXTRACTED', record });
    });
  }
}

let debounceTimer;
function debouncedAttempt() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    attemptExtraction();
  }, 1000);
}

// Observe DOM for changes to catch SPAs
const observer = new MutationObserver(() => {
  debouncedAttempt();
});
observer.observe(document.body, { childList: true, subtree: true });

// Attempt extraction right away as well
debouncedAttempt();
