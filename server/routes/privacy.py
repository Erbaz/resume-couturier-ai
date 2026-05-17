import os
from html import escape
from typing import Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

EXTENSION_NAME = "Resume Couturier AI"
LAST_UPDATED = "May 17, 2026"
CONTACT_EMAIL = os.getenv("PRIVACY_CONTACT_EMAIL", "erbazkamran@gmail.com")
API_HOST = os.getenv(
    "PRIVACY_API_HOST",
    "resume-couturier-ai-server-755081361679.us-central1.run.app",
)

PRIVACY_POLICY_SECTIONS: list[dict[str, Any]] = [
    {
        "id": "overview",
        "title": "Overview",
        "paragraphs": [
            f'{EXTENSION_NAME} (henceforth referred to as "the Extension") helps you tailor resumes and cover letters for job listings on LinkedIn, Indeed, and Glassdoor. This Privacy Policy describes what information we handle, how we use it, and your choices.',
            "By signing in or using the Extension, you agree to this policy. If you do not agree, do not use the Extension.",
        ],
    },
    {
        "id": "collect",
        "title": "Information we collect and use",
        "paragraphs": [
            "We group the data we handle into the categories below. We collect only what is needed to provide the Extension's features.",
        ],
        "list": [
            "<strong>Account information (PII):</strong> When you sign in with Google, we receive your Google account email address and basic profile information (name, profile picture) through Google's OAuth service. Your email is used to authenticate API requests and enforce per-user rate limits.",
            "<strong>Authentication information:</strong> Google OAuth access tokens are used only to authenticate you to our backend. We do not collect or store passwords, PINs, or security questions. Tokens are kept in memory during your session and are not saved in extension local storage.",
            "<strong>Resume and career content (PII):</strong> Resume files you upload, parsed resume text, optional LaTeX templates, additional tailoring instructions, and generated PDFs and cover letters. This may include names, contact details, employment history, education, and similar information from your resume.",
            "<strong>Job listing content (website content):</strong> Text extracted from job postings on supported job-board sites (for example, job descriptions). We do not intentionally collect images, audio, or video from those pages.",
            "<strong>Preferences:</strong> Your selected Gemini model and similar settings stored locally in the Extension.",
            "<strong>Usage data:</strong> A daily request count associated with your email address, stored in server memory for rate limiting (not in a user database).",
        ],
    },
    {
        "id": "local",
        "title": "Data stored on your device",
        "paragraphs": [
            "The Extension stores the following in <code>chrome.storage.local</code> on your device only:",
        ],
        "list": [
            "Parsed resume text",
            "Captured or edited job descriptions",
            "Custom LaTeX template text or uploaded template file data",
            "Additional instructions and Gemini model preference",
        ],
        "paragraphs_after": [
            'This data stays on your device unless you send it to our servers by using features such as "Parse Resume" or "Tailor Resume." You can remove local data by clearing the Extension\'s storage in Chrome or uninstalling the Extension.',
        ],
    },
    {
        "id": "server",
        "title": "Data processed on our servers",
        "paragraphs": [
            f"When you use parse or generate features, resume and job-description content is transmitted over HTTPS to our API at <code>{escape(API_HOST)}</code>. We use it only to fulfill your request (for example, parsing a file or generating a tailored PDF). We do not store resume or job-description content in a database after the request completes.",
            "The only user-related data we retain on the server is your Google account email address and a daily API request count, kept in short-lived in-memory cache (typically up to 24 hours) for rate limiting. We do not operate a persistent user profile database.",
        ],
    },
    {
        "id": "third-parties",
        "title": "Third-party services",
        "paragraphs": [
            "We rely on the following third parties to operate the Extension:",
        ],
        "list": [
            '<strong>Google</strong> — Sign-in (OAuth with <code>openid</code>, <code>email</code>, and <code>profile</code> scopes). Google\'s privacy policy applies to data Google processes: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">policies.google.com/privacy</a>.',
            "<strong>Google Cloud / Vertex AI</strong> — AI processing of resume and job text on our project infrastructure to generate tailored content. Processing is subject to Google Cloud terms and privacy practices.",
            "<strong>Job-board websites</strong> — The Extension reads job-description text from pages you visit on LinkedIn, Indeed, and Glassdoor (and regional variants listed in the Extension manifest). We do not sell data to these sites.",
        ],
        "paragraphs_after": [
            "We do not sell your personal information. We do not use your data for cross-context behavioral advertising.",
        ],
    },
    {
        "id": "permissions",
        "title": "Why the Extension needs certain access",
        "paragraphs": [
            "The Extension requests Chrome permissions to: show the side panel UI; read job descriptions from supported job sites; run scripts on the active tab when you use the Extension; store settings locally; detect navigation between job listings; and sign you in with Google. Host access to our API is required to parse resumes and generate tailored documents.",
        ],
    },
    {
        "id": "retention",
        "title": "Retention",
        "paragraphs": [
            "Local Extension data remains until you delete it or uninstall the Extension.",
            "Server-side rate-limit entries expire from memory when the cache TTL elapses or the server restarts.",
            "Request payloads containing resume or job text are not intentionally retained after your API request finishes.",
        ],
    },
    {
        "id": "security",
        "title": "Security",
        "paragraphs": [
            "API communication uses HTTPS. Access tokens are sent only in Authorization headers to our backend, which validates them with Google before processing requests. No security measure is perfect; use the Extension at your own discretion for sensitive career documents.",
        ],
    },
    {
        "id": "rights",
        "title": "Your choices and rights",
        "paragraphs": [
            "You may log out to clear cached Google tokens from the Extension session.",
            "You may clear locally stored data via Chrome extension settings or by uninstalling the Extension.",
            'You may revoke the Extension\'s access to your Google account in your <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer">Google Account permissions</a> page.',
            "Depending on where you live, you may have rights to access, correct, or delete personal data. Contact us using the information below to make a request.",
        ],
    },
    {
        "id": "children",
        "title": "Children",
        "paragraphs": [
            "The Extension is not directed at children under 13 (or the minimum age required in your jurisdiction). We do not knowingly collect personal information from children.",
        ],
    },
    {
        "id": "changes",
        "title": "Changes to this policy",
        "paragraphs": [
            'We may update this Privacy Policy from time to time. The "Last updated" date at the top will change when we do. Continued use after changes means you accept the updated policy.',
        ],
    },
    {
        "id": "contact",
        "title": "Contact",
        "paragraphs": [],
    },
]

_STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
_CSS_PATH = os.path.join(_STATIC_DIR, "privacy-policy.css")


def _privacy_contact_html() -> str:
    if CONTACT_EMAIL:
        email = escape(CONTACT_EMAIL)
        return f'Questions about this policy: <a href="mailto:{email}">{email}</a>.'
    return (
        "Questions about this policy: contact the developer through the "
        "Chrome Web Store listing support link for this Extension."
    )


def _build_section_html(section: dict[str, Any]) -> str:
    section_id = escape(section["id"])
    title = escape(section["title"])
    html = f'<section class="policy-section" id="{section_id}"><h2>{title}</h2>'

    for paragraph in section.get("paragraphs") or []:
        html += f"<p>{paragraph}</p>"

    items = section.get("list") or []
    if items:
        html += "<ul>"
        for item in items:
            html += f"<li>{item}</li>"
        html += "</ul>"

    for paragraph in section.get("paragraphs_after") or []:
        html += f"<p>{paragraph}</p>"

    html += "</section>"
    return html


def _build_body_html() -> str:
    parts: list[str] = []
    for section in PRIVACY_POLICY_SECTIONS:
        if section["id"] == "contact":
            section = {**section, "paragraphs": [_privacy_contact_html()]}
        parts.append(_build_section_html(section))
    return "".join(parts)


def _load_stylesheet() -> str:
    try:
        with open(_CSS_PATH, encoding="utf-8") as css_file:
            return css_file.read()
    except OSError:
        return ""


def build_privacy_policy_html() -> str:
    stylesheet = _load_stylesheet()
    style_tag = f"<style>{stylesheet}</style>" if stylesheet else ""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Privacy Policy — {escape(EXTENSION_NAME)}</title>
    {style_tag}
  </head>
  <body>
    <main class="policy-page">
      <header class="policy-header">
        <h1>{escape(EXTENSION_NAME)} — Privacy Policy</h1>
        <p class="policy-meta">Last updated: {escape(LAST_UPDATED)}</p>
      </header>
      <div class="policy-body">
        {_build_body_html()}
      </div>
    </main>
  </body>
</html>"""


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    """Public privacy policy page for the Chrome Web Store and extension users."""
    return HTMLResponse(content=build_privacy_policy_html())
