import os
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# Base URL and years to scrape
BASE_URL = "https://papers.nips.cc/"
YEARS = range(2024, 2019, -1)  # From 2024 to 2020
DOWNLOAD_DIR = "NeurIPS_Papers"

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_paper_links(year):
    """Extract paper links from a given NeurIPS year page."""
    url = f"{BASE_URL}paper_files/paper/{year}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch {year} page")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = [
        BASE_URL.rstrip("/") + link.get("href")
        for link in soup.find_all("a")
        if link.get("href") and link.get("href").startswith("/paper_files/paper/") and link.get("href").endswith(".html")
    ]
    
    return links

def download_paper(paper_url, year):
    """Download the PDF of a given paper."""
    response = requests.get(paper_url)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch paper page: {paper_url}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_link = next((BASE_URL.rstrip("/") + link.get("href") for link in soup.find_all("a") if "Paper" in link.text), None)

    if not pdf_link:
        print(f"❌ PDF link not found for {paper_url}")
        return

    # Download PDF
    response = requests.get(pdf_link, stream=True)
    if response.status_code == 200:
        year_folder = os.path.join(DOWNLOAD_DIR, str(year))
        os.makedirs(year_folder, exist_ok=True)
        
        file_name = pdf_link.split("/")[-1]
        file_path = os.path.join(year_folder, file_name)
        
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download PDF: {pdf_link}")

def scrape_year(year):
    """Scrape and download papers for a specific year."""
    print(f"📂 Fetching papers for {year}...")
    paper_links = get_paper_links(year)
    for paper_url in paper_links:
        download_paper(paper_url, year)
    print(f"✅ Completed scraping {year}!")

if __name__ == "__main__":
    # Run multiprocessing for faster execution
    with Pool(processes=len(YEARS)) as pool:
        pool.map(scrape_year, YEARS)

    print("🎉 Scraping completed!")
