# NeurIPS Paper Scraping and Annotation Scripts

This project contains three Python scripts for scraping and analyzing NeurIPS conference papers.

## Scripts Overview

1. **PDF_Scraping.py**
   - Downloads PDF papers from NeurIPS conferences
   - Uses multiprocessing for efficient downloads
   - Organizes papers by year

2. **MetaData_Scraping.py**
   - Extracts metadata (title, authors, abstract) from papers
   - Creates Excel files organized by year
   - Includes error handling and progress tracking

3. **Data_Annotation.py**
   - Uses Google's Gemini AI to categorize papers
   - Adds research category annotations to Excel files
   - Supports multiple research categories

## Requirements

```
beautifulsoup4
requests
openpyxl
google-generativeai
```

## Setup

1. Install dependencies:
   ```bash
   pip install beautifulsoup4 requests openpyxl google-generativeai
   ```

2. Configure API key:
   - Replace the API_KEY in Data_Annotation.py with your Google Gemini API key

## Usage

1. First, download papers:
   ```bash
   python PDF_Scraping.py
   ```

2. Scrape metadata:
   ```bash
   python MetaData_Scraping.py
   ```

3. Annotate papers:
   ```bash
   python Data_Annotation.py
   ```

## Output Structure

- `/NeurIPS_Papers/` - Contains downloaded PDFs organized by year
- `/NeurIPS_Years/` - Contains Excel files with metadata and annotations

## Notes

- Scripts include progress indicators and error handling
- Multiprocessing is used for improved performance
- Excel files are saved incrementally to prevent data loss