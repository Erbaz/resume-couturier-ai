const CAPTURED_JOB_DESCRIPTION_KEY = 'capturedJobDescription';

const JOB_DESCRIPTION_HOST_MAP = {
  'linkedin.com': [
    { pattern: '^JobDetails_AboutTheJob_\\d+$', attribute: 'componentKey' },
    { pattern: 'description__text--rich' },
    { pattern: 'jobs-description-content__text--stretch' }
  ],
  'glassdoor.com': [{ pattern: 'JobDetails_jobDescription__uW_fK' }],
  'indeed.com': [
    { pattern: 'jobsearch-JobComponent-description' },
    { pattern: 'ia-JobDescription' }
  ],
};

function normalizeJobPortalHost(hostname) {
  const h = hostname.toLowerCase();
  if (h === 'linkedin.com' || h.endsWith('.linkedin.com')) {
    return 'linkedin.com';
  }
  if (h === 'glassdoor.com' || h.endsWith('.glassdoor.com')) {
    return 'glassdoor.com';
  }
  if (h === 'indeed.com' || h.endsWith('.indeed.com')) {
    return 'indeed.com';
  }
  return null;
}

function extractJobDescriptionInPage(selectorList) {
  for (const spec of selectorList) {
    // Default to 'class' attribute if none specified
    const attr = spec.attribute || spec.identifier || 'class';
    const pattern = spec.pattern || spec.valuePattern;
    if (!pattern) continue;

    const regex = new RegExp(pattern);
    const nodes = document.querySelectorAll('*');

    for (let i = 0; i < nodes.length; i++) {
      const el = nodes[i];
      let val = el.getAttribute(attr);
      if (val == null && attr in el) {
        val = el[attr];
      }
      
      if (typeof val === 'string' && regex.test(val)) {
        return {
          ok: true,
          html: el.innerHTML,
          text: (el.innerText || '').trim(),
        };
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
let lastAttemptTime = 0;
const MAX_WAIT = 2000; // Force run every 2s even if DOM stays busy

function debouncedAttempt() {
  const now = Date.now();
  clearTimeout(debounceTimer);

  // If it's been a while since we actually ran extraction, run it now
  if (now - lastAttemptTime > MAX_WAIT) {
    lastAttemptTime = now;
    attemptExtraction();
  } else {
    // Otherwise, set a timer to run it soon
    debounceTimer = setTimeout(() => {
      lastAttemptTime = Date.now();
      attemptExtraction();
    }, 500);
  }
}

// Observe DOM for changes to catch SPAs
const observer = new MutationObserver(() => {
  debouncedAttempt();
});
observer.observe(document.body, { childList: true, subtree: true });

// Attempt extraction right away as well
debouncedAttempt();
