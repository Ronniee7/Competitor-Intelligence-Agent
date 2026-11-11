import ipaddress
import socket

from urllib.parse import urlparse


def validate_public_url(url: str) -> str:
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if not parsed.hostname:
        raise ValueError("URL must contain a hostname.")

    hostname = parsed.hostname

    if hostname.lower() == "localhost":
        raise ValueError("Localhost URLs are not allowed.")

    try:
        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise ValueError("Unable to resolve hostname.") from exc

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if not ip.is_global:
            raise ValueError(
                "Private, local and non-public IP addresses are forbidden."
            )

    return url