import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_any_page_content(url):
    """Fetch content from a URL, handling both static and dynamic pages."""
    try:
        # Attempt static fetching first
        content = fetch_static_page_content(url)
        if content and len(content.strip()) > 500:  # Assume valid if content is sufficient
            return content
    except Exception as e:
        print(f"Static fetch failed: {e}")

    # Fallback to dynamic fetching for JavaScript-heavy pages
    try:
        content = fetch_dynamic_page_content(url)
        if content:
            return content
    except Exception as e:
        print(f"Dynamic fetch failed: {e}")

    raise RuntimeError("Failed to fetch content from the URL using both methods.")

def fetch_static_page_content(url):
    """Fetch and preprocess content from a static documentation page."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise error for bad HTTP responses
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary elements
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    # Extract text content
    text_content = soup.get_text(separator="\n")
    return clean_and_structure_content(text_content)

def fetch_dynamic_page_content(url):
    """Fetch content from a dynamically rendered page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=20000)  # Timeout for dynamic loading
        html = page.content()  # Get fully rendered HTML
        browser.close()
    return parse_dynamic_page_content(html)

def parse_dynamic_page_content(html):
    """Parse dynamically rendered HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
    text_content = soup.get_text(separator="\n")
    return clean_and_structure_content(text_content)

def clean_and_structure_content(text):
    """Clean and structure the extracted text content."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    structured_text = "\n".join(lines)
    return structured_text[:10000]  # Limit content to first 10,000 characters



if __name__ == "__main__":
    test_url = "https://python.langchain.com/v0.1/docs/integrations/llms/"
    try:
        content = fetch_any_page_content(test_url)
        print("Fetched Content:\n", content)
    except Exception as e:
        print("Error fetching content:", e)
