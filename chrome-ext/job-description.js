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
  const results = [];
  for (const spec of selectorList) {
    const attr = spec.attribute || spec.identifier || 'class';
    const pattern = spec.pattern || spec.valuePattern;
    if (!pattern) continue;

    const regex = new RegExp(pattern);
    
    // Optimization: If searching for a class and pattern is a simple string, use getElementsByClassName
    let candidates = [];
    if (attr === 'class' && /^[a-zA-Z0-9\-_]+$/.test(pattern)) {
      candidates = Array.from(document.getElementsByClassName(pattern));
    } else if (attr === 'class') {
       // Possibly multiple classes or partial match, use querySelectorAll if it's not a complex regex
       try {
         candidates = Array.from(document.querySelectorAll(`[class*="${pattern}"]`));
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
        return {
          ok: true,
          html: el.innerHTML,
          text: (el.innerText || '').trim(),
          tagName: el.tagName,
          id: el.id,
          className: el.className
        };
      }
    }
  }
  return { ok: false, checkedCount: document.querySelectorAll('*').length };
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
      console.warn('[runLiveJDCheck] No active tab info found.');
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

    // Run in all frames because some portals (like LinkedIn Job Hub) might use iframes
    const injectedResults = await chrome.scripting.executeScript({
      target: { tabId: tab.id, allFrames: true },
      func: extractJobDescriptionInPage,
      args: [JOB_DESCRIPTION_HOST_MAP[portalHost]],
    });

    // Find the first frame that returned a successful result
    let result = null;
    if (injectedResults && injectedResults.length > 0) {
      for (const frameResult of injectedResults) {
        if (frameResult.result && frameResult.result.ok) {
          result = frameResult.result;
          break;
        }
      }
    }

    let isStaleDom = false;
    const lastJD = await getStoredCapturedJobDescription();
    if (result && result.ok && result.text && lastJD && lastJD.text === result.text) {
      if (lastJD.sourceUrl) {
        const oldUrl = new URL(lastJD.sourceUrl);
        const newUrl = new URL(tab.url);
        const oldId = oldUrl.searchParams.get('currentJobId') || oldUrl.pathname;
        const newId = newUrl.searchParams.get('currentJobId') || newUrl.pathname;
        if (oldId !== newId) {
          isStaleDom = true;
        }
      }
    }

    if (result && result.ok && result.text && !isStaleDom) {
      const record = {
        portal: portalHost,
        sourceUrl: tab.url,
        html: result.html,
        text: result.text,
        capturedAt: Date.now(),
      };
      await saveCapturedJobDescription(record);
      const jdTextEl = document.getElementById('jobDescriptionText');
      if (jdTextEl) jdTextEl.value = record.text;
      if (jdStatus) jdStatus.innerHTML = '<span style="color: #0f9d58;">Updated JD!</span>';
    } else {
      // If not found and we still have retries or we are on the same supported portal URL
      if (retryCount > 0) {
        const reason = isStaleDom ? 'Stale DOM detected' : 'JD not found';
        if (jdStatus) jdStatus.innerHTML = `<span style="color: #1a73e8;">Waiting for job details... (${retryCount}s left)</span>`;
        setTimeout(() => runLiveJDCheck(expectedUrl, retryCount - 1, delayMs), delayMs);
      } else {
        console.warn('[runLiveJDCheck] Polling timed out.');
        if (jdStatus) jdStatus.innerHTML = 'Timed out searching for JD &mdash; keeping old JD state.';
      }
    }
  } catch (err) {
    console.warn('Live JD check failed:', err);
    if (jdStatus) jdStatus.innerHTML = 'Unable to detect a new JD &mdash; keeping old JD state.';
  }
}
