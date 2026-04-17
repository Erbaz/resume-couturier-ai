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

async function generateResume(templateId, parsedResumeText, geminiModel, jobDesc, customInstructions, templateLatex) {
  if (!authToken) {
    throw new Error('Missing auth token. Please sign in again.');
  }

  const response = await fetch(`${API_BASE}/resume/generate`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_info: parsedResumeText,
      job_desc: jobDesc || '',
      custom_instructions: customInstructions || '',
      gemini_model: geminiModel,
      template_id: templateId || null,
      template_latex: templateLatex || null,
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

  const missingKeywords = decodeURIComponent(response.headers.get('x-ats-missing-keywords') || '');
  const coverLetter = decodeURIComponent(response.headers.get('x-cover-letter') || '');
  const pdfBlob = await response.blob();
  return { missingKeywords, coverLetter, pdfBlob };
}
