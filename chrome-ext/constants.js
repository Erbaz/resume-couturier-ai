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
