import requests
from bs4 import BeautifulSoup
import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def extract_summary(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.string.strip() if soup.title else 'No title found.'
    meta_desc = soup.find('meta', attrs={'name':'description'})
    description = meta_desc['content'].strip() if meta_desc else 'No description available.'

    return f"{title}: {description}"

if __name__ == "__main__":
    while True:
        clear()
        domain = input("Enter the domain name (e.g., example.com): ").strip()
        if domain == 'exit':
            sys.exit()
        print(f"\nAnalyzing {domain}...")
        content = fetch_website(domain)
        if content:
            summary = extract_summary(content)
            print("\nSummary about the site:")
            print(summary)
        input("\nPress Enter to continue...")
