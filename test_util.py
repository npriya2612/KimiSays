#test_util.py
from bot.util import extract_text_from_pdf, extract_text_from_url
import os
# List of PDF files
pdf_files = [
    r'C:\chatbot_project\data\AWS Validator setup procedure.pdf'
]

# List of URLs
urls = [
    'https://www.alkimi.org/how-it-works'
]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        try:
            pdf_text = extract_text_from_pdf(pdf_file)
            print(f"PDF Text ({pdf_file}):\n", pdf_text)  # Print entire content
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
    else:
        print(f"File not found: {pdf_file}")

for url in urls:
    try:
        url_text = extract_text_from_url(url)
        print(f"URL Text ({url}):\n", url_text)  # Print entire content
    except Exception as e:
        print(f"Error processing {url}: {e}")
