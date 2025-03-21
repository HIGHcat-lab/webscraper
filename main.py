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

def fetch_wikipedia_info(company_name):
    search_url = f"https://en.wikipedia.org/wiki/{company_name.replace(' ', '_')}"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        info_box = soup.find('table', {'class': 'infobox'})
        if not info_box:
            return "No Wikipedia infobox found."

        info = {}
        for row in info_box.find_all('tr'):
            header = row.find('th')
            value = row.find('td')
            if header and value:
                key = header.text.strip()
                val = value.text.strip().replace('\n', ', ')
                info[key] = val

        details = ""
        for item in ['Founded', 'Founder', 'Headquarters', 'Area served', 'Key people', 'Industry']:
            if item in info:
                details += f"{item}: {info[item]}\n"

        return details if details else "No detailed info found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching Wikipedia data: {e}"

if __name__ == "__main__":
    while True:
        clear()
        domain = input("Enter the domain name (e.g., example.com) or 'exit' to quit: ").strip()
        if domain.lower() == 'exit':
            clear()
            sys.exit()

        print(f"\nAnalyzing {domain}...")
        content = fetch_website(domain)
        if content:
            summary = extract_summary(content)
            print("\nWebsite Summary:")
            print(summary)

            company_name = domain.split('.')[0]
            print("\nFetching additional information from Wikipedia...")
            wiki_info = fetch_wikipedia_info(company_name)
            print("\nWikipedia Information:")
            print(wiki_info)

        input("\nPress Enter to continue...")
