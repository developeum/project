import requests


def shorten_url(long_url: str) -> str:
    """
        Shorten URL with bit.ly service
    """

    api_url = 'https://cutt.ly/scripts/shortenUrl.php'

    link = requests.post(api_url, data={
        'url': long_url,
        'domain': 0
    }).text

    return link
