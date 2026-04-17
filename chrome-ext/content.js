const CAPTURED_JOB_DESCRIPTION_KEY = 'capturedJobDescription';

const JOB_DESCRIPTION_HOST_MAP = {
  'linkedin': [
    { pattern: '^JobDetails_AboutTheJob_\\d+$', attribute: 'componentKey' },
    { pattern: 'description__text--rich' },
    { pattern: 'jobs-description-content__text--stretch' }
  ],
  'glassdoor': [
    { pattern: '^JobDetails_jobDescription__' },
    { pattern: '^Section_sectionComponent__' }
  ],
  'indeed': [
    { pattern: 'jobsearch-JobComponent-description' },
    { pattern: 'ia-JobDescription' }
  ],
};

function normalizeJobPortalHost(hostname) {
  const h = hostname.toLowerCase();
  if (/(^|\.)linkedin\./.test(h)) {
    return 'linkedin';
  }
  if (/(^|\.)glassdoor\./.test(h)) {
    return 'glassdoor';
  }
  if (/(^|\.)indeed\./.test(h)) {
    return 'indeed';
  }
  return null;
}

function extractJobDescriptionInPage(selectorList) {
  for (const spec of selectorList) {
    const attr = spec.attribute || spec.identifier || 'class';
    const pattern = spec.pattern || spec.valuePattern;
    if (!pattern) continue;

    const regex = new RegExp(pattern);
    
    let candidates = [];
    if (attr === 'class' && /^[a-zA-Z0-9\-_]+$/.test(pattern)) {
      candidates = Array.from(document.getElementsByClassName(pattern));
    } else if (attr === 'class') {
       try {
         // Extract the literal part of the regex to use in querySelectorAll for efficiency
         const literalPart = pattern.replace(/[^^a-zA-Z0-9\-_].*$/, '').replace(/^\^/, '');
         candidates = Array.from(document.querySelectorAll(`[class*="${literalPart}"]`));
       } catch(e) {
         candidates = Array.from(document.querySelectorAll('*'));
       }
    } else {
      candidates = Array.from(document.querySelectorAll('*'));
    }

    for (const el of candidates) {
      let val = el.getAttribute(attr);
      if (val == null && attr in el) {
        val = el[attr];
      }
      
      if (typeof val === 'string' && regex.test(val)) {
        console.log('[RC-AI] Match found! Pattern:', pattern, 'Actual Attribute Value:', val);
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

  console.log('[RC-AI] Extraction attempt for:', portalHost, 'on', window.location.hostname);

  const selectorList = JOB_DESCRIPTION_HOST_MAP[portalHost];
  if (!selectorList?.length) return;

  const result = extractJobDescriptionInPage(selectorList);
  if (result.ok && result.text) {
    if (result.text !== lastExtractedText) {
      lastExtractedText = result.text;
      const record = {
        portal: portalHost,
        sourceUrl: window.location.href,
        html: result.html,
        text: result.text,
        capturedAt: Date.now(),
      };
      chrome.storage.local.set({ [CAPTURED_JOB_DESCRIPTION_KEY]: record }, () => {
        // Notify components like the side panel that JD has been updated via DOM change
        chrome.runtime.sendMessage({ type: 'JD_EXTRACTED', record });
      });
    } 
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
const observer = new MutationObserver((mutations) => {
  debouncedAttempt();
});
observer.observe(document.body, { childList: true, subtree: true, characterData: true });

// Attempt extraction right away as well
debouncedAttempt();
