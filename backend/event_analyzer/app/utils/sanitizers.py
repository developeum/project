from html import unescape as html_unescape
import re

replaces = {
    '\u00a0': ' ',
    '\u00bb': '"',
    '\u00ab': '"',
    '\u201c': '"',
    '\u201d': '"',
    '\u200b': '',
}

def sanitize(text: str):
    """
        Sanitize text removing html encoded parts, double spaces and so on
    """

    if text is None:
        return None

    text = html_unescape(html_unescape(text))

    for key, value in replaces.items():
        text = text.replace(key, value)

    text = re.sub(r'[ \t]+', ' ', text).strip()

    return text
