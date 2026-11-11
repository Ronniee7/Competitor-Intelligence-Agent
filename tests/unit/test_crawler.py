import httpx
import pytest

from app.ingestion.crawler import WebsiteCrawler


@pytest.mark.asyncio
async def test_fetch_page(monkeypatch):

    html = """
    <html>
        <head>
            <title>Competitor Website</title>
        </head>
        <body>
            <h1>Our Services</h1>
            <p>We provide business solutions.</p>
        </body>
    </html>
    """

    async def mock_handler(request):

        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text=html,
            request=request,
        )

    transport = httpx.MockTransport(mock_handler)

    monkeypatch.setattr(
        "app.ingestion.crawler.validate_public_url",
        lambda url: url,
    )

    crawler = WebsiteCrawler(transport=transport)

    result = await crawler.fetch_page(
        "https://example.com"
    )

    assert result.status_code == 200

    assert result.title == "Competitor Website"

    assert "business solutions" in result.content