from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from middleware.authMiddleware import verify_google_oauth_token

router = APIRouter()


class ScrapeJobDescriptionRequest(BaseModel):
    url: str


class LinkedInDescriptionParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.capture_depth = 0
        self.matched = False
        self.html_parts: list[str] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = set((attrs_dict.get("class") or "").split())
        is_target = (
            tag == "div"
            and "description__text" in classes
            and "description__text--rich" in classes
        )

        if is_target and self.capture_depth == 0:
            self.matched = True
            self.capture_depth = 1
            self.html_parts.append(self.get_starttag_text() or "<div>")
            return

        if self.capture_depth > 0:
            self.capture_depth += 1
            self.html_parts.append(self.get_starttag_text() or f"<{tag}>")

    def handle_endtag(self, tag):
        if self.capture_depth > 0:
            self.html_parts.append(f"</{tag}>")
            self.capture_depth -= 1

    def handle_data(self, data):
        if self.capture_depth > 0:
            self.html_parts.append(data)
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

    def handle_entityref(self, name):
        if self.capture_depth > 0:
            entity = f"&{name};"
            self.html_parts.append(entity)
            self.text_parts.append(unescape(entity))

    def handle_charref(self, name):
        if self.capture_depth > 0:
            entity = f"&#{name};"
            self.html_parts.append(entity)
            self.text_parts.append(unescape(entity))


def linkedin_job_description_extractor(html: str) -> dict:
    parser = LinkedInDescriptionParser()
    parser.feed(html)
    parser.close()

    if not parser.matched:
        raise HTTPException(
            status_code=404,
            detail=(
                "Could not find LinkedIn job description container "
                "(div.description__text.description__text--rich)."
            ),
        )

    extracted_html = "".join(parser.html_parts).strip()
    extracted_text = "\n".join(parser.text_parts).strip()
    return {"html": extracted_html, "text": extracted_text}


def get_portal_from_url(url: str) -> str:
    hostname = (urlparse(url).hostname or "").lower()
    if "linkedin.com" in hostname:
        return "linkedin"
    return "unknown"


@router.post("/scrape/job-description")
async def scrape_job_description(
    body: ScrapeJobDescriptionRequest,
    token_data: dict = Depends(verify_google_oauth_token),
):
    parsed_url = urlparse(body.url)
    if parsed_url.scheme not in {"http", "https"}:
        raise HTTPException(status_code=400, detail="Only http/https URLs are supported")

    portal = get_portal_from_url(body.url)
    if portal == "unknown":
        raise HTTPException(status_code=400, detail="Unsupported job portal")

    try:
        response = requests.get(
            body.url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch URL: {exc}") from exc

    if portal == "linkedin":
        extracted = linkedin_job_description_extractor(response.text)
    else:
        raise HTTPException(status_code=400, detail="Unsupported job portal")

    return {
        "portal": portal,
        "source_url": body.url,
        "extracted_html": extracted["html"],
        "extracted_text": extracted["text"],
    }
