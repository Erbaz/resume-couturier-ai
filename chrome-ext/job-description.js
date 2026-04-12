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

function queryActiveTab() {
  return new Promise((resolve) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs?.[0] || null);
    });
  });
}

let lastStartedPollingUrl = null;

async function runLiveJDCheck(expectedUrl = null, retryCount = 30, delayMs = 1000) {
  try {
    const tab = await queryActiveTab();
    if (!tab || !tab.id || !tab.url) {
      if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
      return;
    }

    // If this is the first call, set the expected URL
    if (expectedUrl === null) {
      expectedUrl = tab.url;
      lastStartedPollingUrl = expectedUrl;
    }

    // Stop if the user has navigated to a different URL since this poll started
    if (lastStartedPollingUrl !== expectedUrl) {
      return; 
    }

    const hostname = new URL(tab.url).hostname;
    const portalHost = normalizeJobPortalHost(hostname);
    
    // Only continue polling if we are on a supported job portal
    if (!portalHost || !JOB_DESCRIPTION_HOST_MAP[portalHost]) {
      if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
      return;
    }

    if (jdStatus) {
      jdStatus.innerHTML = `<span style="color: #1a73e8;">Checking for JD... ${retryCount > 0 ? '(polling)' : ''}</span>`;
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
      // If not found and we still have retries or we are on the same supported portal URL
      if (retryCount > 0) {
        if (jdStatus) jdStatus.innerHTML = `<span style="color: #1a73e8;">Waiting for job details... (${retryCount}s left)</span>`;
        setTimeout(() => runLiveJDCheck(expectedUrl, retryCount - 1, delayMs), delayMs);
      } else {
        if (jdStatus) jdStatus.innerHTML = 'Timed out searching for JD &mdash; keeping old JD state.';
      }
    }
  } catch (err) {
    console.warn('Live JD check failed:', err);
    if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
  }
}
