import fitz  # PyMuPDF
from docx import Document
import requests
from bs4 import BeautifulSoup
import os


def extract_text_from_pdf(file_path, save_to_file=True, output_dir=None):
    """
    Extracts text from a PDF and optionally appends it to a file.
    
    :param file_path: Path to the PDF file
    :param save_to_file: Boolean indicating whether to save the text to a file (default: True)
    :param output_dir: Directory to save the extracted text file (optional)
    :return: Extracted text
    """
    document = fitz.open(file_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    
    if save_to_file:
        try:
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, 'extracted_text.txt')
            else:
                output_path = 'extracted_text.txt'
            
            with open(output_path, 'a', encoding='utf-8') as file:
                file.write(text + '\n\n')  # Add two newlines between pages
            
            print(f"Successfully saved extracted text to {output_path}")
        except Exception as e:
            print(f"Failed to save extracted text to {output_path}: {e}")

    return text

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def extract_text_from_url(url):
    """
    Extract all visible text content from a URL using Selenium and BeautifulSoup.
    
    Args:
    - url (str): URL to extract text from.
    
    Returns:
    - str: Extracted and cleaned text content from the webpage.
    """
    try:
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')  # Ignore certificate errors
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        retries = 3
        for i in range(retries):
            try:
                driver.get(url)
                time.sleep(5)  # Adjust time to wait for dynamic content to load
                break
            except Exception as e:
                if i == retries - 1:
                    raise Exception(f"Failed to retrieve content from {url} after {retries} attempts: {str(e)}")
                time.sleep(2)  # Wait before retrying
        
        # Get page source after loading
        page_source = driver.page_source
        driver.quit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find specific elements or sections based on HTML structure
        main_content = soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        # Extract text from the found elements
        extracted_text = ' '.join([element.get_text(separator=' ', strip=True) for element in main_content])

        return extracted_text
    
    except Exception as e:
        raise Exception(f"Failed to retrieve content from {url}: {str(e)}")

