from urllib.parse import urlparse

IMPORTANT_KEYWORDS = [
    "about",
    "product",
    "service",
    "pricing",
    "solution",
    "industry",
    "customer",
    "partner",
    "news",
    "blog",
    "company",
]

def discover_relevant_links(
    links: list[str],
    base_url: str,
    max_pages: int = 10,
):

    base_domain = urlparse(base_url).netloc

    relevant = []

    for link in links:

        parsed = urlparse(link)

        # Stay on the original website.
        if parsed.netloc != base_domain:
            continue

        path = parsed.path.lower()

        if any(
            keyword in path
            for keyword in IMPORTANT_KEYWORDS
        ):

            clean_url = parsed._replace(
                query="",
                fragment="",
            ).geturl()

            if clean_url not in relevant:
                relevant.append(clean_url)

    return relevant[:max_pages]