from bs4 import BeautifulSoup
import re

def extract_body_content(html_content):
    """
    Extracts and cleans the content inside the <body> tag.
    Removes non-essential tags like <script> and <style>.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract <body> content
    body = soup.body
    if not body:
        raise ValueError("No <body> tag found in the HTML content.")

    # Remove unwanted tags
    for tag in body(["script", "style", "meta", "noscript"]):
        tag.decompose()  # Remove the tag completely

    # Optionally remove navigation and footer sections
    for tag in body.find_all(["nav", "footer"]):
        tag.decompose()

    # Get cleaned text content
    text_content = body.get_text(separator="\n", strip=True)

    # Optionally truncate if too long (e.g., 4096 tokens)
    max_length = 5000  # Example token limit; adjust as needed
    if len(text_content) > max_length:
        text_content = text_content[:max_length] + "\n[Content truncated]"

    return text_content
