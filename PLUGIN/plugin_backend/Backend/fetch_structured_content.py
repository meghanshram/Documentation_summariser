import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
from urllib.parse import urlparse

def fetch_content(url):
    """Fetch content in JSON, HTML, or dynamically rendered HTML."""
    try:
        # Try fetching JSON
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.headers.get("Content-Type", "").startswith("application/json"):
            return {"type": "json", "content": response.json()}  # JSON content

        # Fetch HTML if JSON is not available
        return {"type": "html", "content": response.text}  # Raw HTML content

    except requests.exceptions.RequestException as e:
        print(f"Static fetch failed: {e}")

    # Dynamic rendering fallback
    try:
        html = fetch_dynamic_content(url)
        return {"type": "html", "content": html}
    except Exception as e:
        raise RuntimeError(f"Failed to fetch content: {e}")

def fetch_dynamic_content(url):
    """Fetch dynamically rendered HTML using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=20000)  # Wait for full load
        content = page.content()  # Rendered HTML
        browser.close()
    return content

def save_to_file(content, url, content_type):
    """Save the fetched content to a file."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace(":", "_")  # Replace ':' for Windows compatibility

    # Determine file extension based on content type
    extension = "json" if content_type == "json" else "html"
    file_name = f"{domain}.{extension}"

    # Create an output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", file_name)

    # Write content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        if content_type == "json":
            import json
            json.dump(content, file, indent=4)  # Pretty-print JSON
        else:
            file.write(content)  # Write HTML as-is

    print(f"Content from {url} saved to {file_path}")


# if __name__ == "__main__":
#     # Test cases
#     url="https://python.langchain.com/v0.1/docs/integrations/llms/"

#     try:
#         result = fetch_content(url)
#         if result["type"] == "json":
#             save_to_file(result["content"], url, "json")
#         elif result["type"] == "html":
#             save_to_file(result["content"], url, "html")
#             html_str=extract_body_content(result["content"])
#             # with open("output.txt","w") as file:
#             #     file.write(html_str)
#             print(html_str)
#     except Exception as e:
#         print(f"Error fetching from {url}: {e}")
