import os
import requests
import openpyxl
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re

# Base URL
BASE_URL = "https://papers.nips.cc/"
YEARS = list(range(2024, 1986, -1))  # Convert range to a list
OUTPUT_DIR = "NeurIPS_Years"  # Folder to store per-year Excel files

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to clean non-printable characters
def replace_illegal_chars(text):
    """Removes non-printable characters for Excel compatibility."""
    if not text:
        return "N/A"
    return re.sub(r'[^\x20-\x7E]', '', text).strip()  # Keeps only printable ASCII characters

def get_paper_links(year):
    """Extract paper links from a given NeurIPS year page."""
    url = f"{BASE_URL}paper_files/paper/{year}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent bot detection

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch {year} page (Status: {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        BASE_URL.rstrip("/") + link.get("href")
        for link in soup.find_all("a")
        if link.get("href") and link.get("href").startswith("/paper_files/paper/") and link.get("href").endswith(".html")
    ]

def scrape_year(year):
    """Scrape all papers for a specific year and save to an Excel file after each entry."""
    print(f"📅 Scraping papers for {year}...")

    paper_links = get_paper_links(year)
    if not paper_links:
        print(f"❌ No papers found for {year}")
        return
    
    # Create an Excel file for this year
    xlsx_file = os.path.join(OUTPUT_DIR, f"NeurIPS_{year}.xlsx")
    
    # Initialize workbook and worksheet
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = f"NeurIPS {year}"
    sheet.append(["Sr. No", "Year", "Title", "Authors", "Abstract", "PDF Link"])  # Header row
    wb.save(xlsx_file)  # Save the empty sheet first

    sr_no = 1  # Serial number counter

    for paper_url in paper_links:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(paper_url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch paper page: {paper_url} (Status: {response.status_code})")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract paper title
        title_tag = soup.find("h4")
        title = replace_illegal_chars(title_tag.text) if title_tag else "Unknown Title"

        # Extract authors
        authors = "Unknown Authors"
        author_h4 = soup.find("h4", string="Authors")
        if author_h4:
            author_p = author_h4.find_next_sibling("p")
            if author_p:
                authors = replace_illegal_chars(author_p.text)

        # Extract abstract
        abstract = "No Abstract Found"
        abstract_h4 = soup.find("h4", string="Abstract")
        if abstract_h4:
            abstract_p = abstract_h4.find_next_sibling("p")
            if abstract_p:
                abstract = replace_illegal_chars(abstract_p.text)
        
        # Extract PDF link
        pdf_link = next((BASE_URL.rstrip("/") + link.get("href") for link in soup.find_all("a") if "Paper" in link.text), None)

        if pdf_link:
            # Append the new data row
            sheet.append([sr_no, year, title, authors, abstract, pdf_link])
            wb.save(xlsx_file)  # Save after every entry
            print(f"✅ {year} | {sr_no}: {title} - Authors: {authors}")
            sr_no += 1  # Increment serial number
        else:
            print(f"❌ PDF link not found for {paper_url}")

if __name__ == "__main__":
    # Use multiprocessing to scrape years in parallel
    with Pool(processes=len(YEARS)) as pool:
        pool.map(scrape_year, YEARS)  # Ensure YEARS is a list

    print("🎉 Scraping completed for all years!")
