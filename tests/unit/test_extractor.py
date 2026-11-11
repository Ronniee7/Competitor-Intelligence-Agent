from app.ingestion.extractor import extract_page


def test_extract_page():

    html = """
    <html>
        <head>
            <title>Test Fintech Company</title>
            <meta name="description"
                  content="Digital payment solutions">
        </head>

        <body>
            <nav>Navigation</nav>

            <h1>Our Products</h1>

            <h2>Payment Processing</h2>

            <p>We provide payment infrastructure.</p>

            <a href="/about">About Us</a>

            <script>alert("unwanted")</script>
        </body>
    </html>
    """

    result = extract_page(
        html=html,
        url="https://example.com",
        status_code=200,
    )

    assert result.title == "Test Fintech Company"

    assert result.description == "Digital payment solutions"

    assert "Our Products" in result.headings

    assert "payment infrastructure" in result.content

    assert "alert" not in result.content

    assert "https://example.com/about" in result.links

    assert len(result.content_hash) == 64