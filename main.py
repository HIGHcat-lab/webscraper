#beta

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_website(domain):
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain
    try:
        response = requests.get(domain, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def summarize_website(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.string.strip() if soup.title else 'No title found'
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    meta_desc = meta_desc['content'].strip() if meta_desc and 'content' in meta_desc.attrs else 'No description found.'

    headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])][:5]

    print(f"\nWebsite Title: {title}")
    print(f"\nMeta Description: {meta_desc}\n")

    if headings:
        print("Top Headings on the Page:")
        for idx, heading in enumerate(headings, start=1):
            print(f"{idx}. {heading}")
    else:
        print("No prominent headings found.")

if __name__ == "__main__":
    domain = input("Enter the domain name (e.g., example.com): ").strip()
    print(f"\nFetching information from {domain}...")
    content = fetch_website(domain)
    if content:
        summarize_website(content)

