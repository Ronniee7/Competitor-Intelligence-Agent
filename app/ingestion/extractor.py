import hashlib

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.models.research import ExtractedPage


def extract_page(html: str, url: str, status_code: int) -> ExtractedPage:

    soup = BeautifulSoup(html, "lxml")

    # Remove unnecessary HTML elements.
    for element in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "nav",
        "footer",
    ]):
        element.decompose()

    # Extract page title.
    title = None

    if soup.title:
        title = soup.title.get_text(strip=True)

    # Extract meta description.
    description = None

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description:
        description = meta_description.get("content")

    # Extract headings.
    headings = [
        heading.get_text(" ", strip=True)
        for heading in soup.find_all(["h1", "h2", "h3"])
        if heading.get_text(strip=True)
    ]

    # Extract paragraphs.
    paragraphs = [
        paragraph.get_text(" ", strip=True)
        for paragraph in soup.find_all("p")
        if paragraph.get_text(strip=True)
    ]

    # Extract links.
    links = []

    for anchor in soup.find_all("a", href=True):

        absolute_url = urljoin(url, anchor["href"])

        if absolute_url.startswith(("http://", "https://")):
            links.append(absolute_url)

    # Construct clean text.
    content = soup.get_text(separator="\n", strip=True)

    # Remove repeated whitespace.
    content = "\n".join(
        line.strip()
        for line in content.splitlines()
        if line.strip()
    )

    # Generate content fingerprint.
    content_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    return ExtractedPage(
        url=url,
        title=title,
        description=description,
        headings=headings,
        paragraphs=paragraphs,
        links=list(dict.fromkeys(links)),
        content=content,
        status_code=status_code,
        content_hash=content_hash,
    )