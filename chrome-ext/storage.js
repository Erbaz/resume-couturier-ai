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
