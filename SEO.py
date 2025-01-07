import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def check_website_performance(base_url):
    """
    Function to check website performance for all pages linked from the base URL.
    Generates a DataFrame with performance metrics for each page.

    Parameters:
        base_url (str): The base URL of the website.

    Returns:
        DataFrame: A pandas DataFrame with performance metrics.
    """
    try:
        # Measure performance for the base URL
        start_time = time.time()
        response = requests.get(base_url)
        base_load_time = time.time() - start_time

        if response.status_code != 200:
            print(f"Error accessing {base_url}, Status code: {response.status_code}")
            return

        # Parse the base URL content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Prepare data collection
        data = []

        # Check performance for each link
        for link in links:
            try:
                start_time = time.time()
                page_response = requests.get(link)
                load_time = time.time() - start_time

                data.append({
                    'URL': link,
                    'Status Code': page_response.status_code,
                    'Load Time (s)': round(load_time, 2),
                    'Content Length (KB)': round(len(page_response.content) / 1024, 2)
                })
            except Exception as e:
                data.append({
                    'URL': link,
                    'Status Code': 'Error',
                    'Load Time (s)': None,
                    'Content Length (KB)': None,
                    'Error': str(e)
                })

        # Convert to DataFrame
        df = pd.DataFrame(data)
        print(df)
        return df.to_string()

    except Exception as e:
        print(f"An error occurred: {e}")
        return

def scrape_all_texts(base_url):
    """
    Function to scrape all texts from all pages linked from the base URL and save to a text file.

    Parameters:
        base_url (str): The base URL of the website.

    Returns:
        str: All scraped text as a single string.
    """
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Error accessing {base_url}, Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Scrape text from all links
        all_text = ""
        document_structure = []

        for link in links:
            try:
                page_response = requests.get(link)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    page_title = page_soup.title.string if page_soup.title else "No Title"
                    page_text = page_soup.get_text(separator='\n', strip=True)
                    all_text += f"### {page_title} ({link})\n\n{page_text}\n\n"
                    document_structure.append(f"### {page_title} ({link})\n\n{page_text}\n\n")
            except Exception as e:
                print(f"Error scraping {link}: {e}")

        # Save to text file
        with open('website_texts.txt', 'w', encoding='utf-8') as file:
            for section in document_structure:
                file.write(section)

        print("All website texts saved to 'website_texts.txt'")
        return all_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return


