function setParseStatus(message, isError) {
  parseStatus.textContent = message;
  parseStatus.style.color = isError ? '#c5221f' : '#666';
}

function setGenerationStatus(message, isError) {
  generationStatus.textContent = message;
  generationStatus.style.color = isError ? '#c5221f' : '#666';
}

function setTemplatesStatus(message, isError) {
  templatesStatus.textContent = message;
  templatesStatus.style.color = isError ? '#c5221f' : '#666';
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
  // Append a timestamp to bypass browser caching for updated thumbnails
  return `${API_BASE}/assets/${name}?t=${Date.now()}`;
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
