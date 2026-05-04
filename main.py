import pdfplumber
import os
import re
from dotenv import load_dotenv

load_dotenv()

PDF_PASSWORD = os.getenv('PDF_PASSWORD')
PDF_PATH = 'pdf/3055_marzec_2026.pdf'

def get_lines(pdf) -> list[str]:
    all_lines = []

    for page in pdf.pages:
        text = page.extract_text()
        lines = text.splitlines()
        all_lines.extend(lines)

    return all_lines

def is_transaction_line(line: str) -> bool:
    date_pattern = r"^\d{2}-\d{2}-\d{4}"
    operation_keywords = ['ZAKUPPRZYUŻYCIUKARTY', 
                          'PRZELEWWŁASNY',
                          'BLIKP2P-WYCHODZĄCY',
                          'AUTOMATYCZNASPŁATAKARTY',
                          'WYPŁATAWBANKOMACIE', 
                          'PROWIZJA',
                          'BLIKZAKUPE-COMMERCE',
                          ]
    return (bool(re.match(date_pattern, line)) 
            and any(keyword in line for keyword in operation_keywords))

def main():

    with pdfplumber.open(PDF_PATH, password=PDF_PASSWORD) as pdf:
        
        lines = get_lines(pdf)

        for line in lines:
            if is_transaction_line(line):
                print(repr(line))        


if __name__ == "__main__":
    main()