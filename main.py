import pdfplumber
import os
import re
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

PDF_PASSWORD = os.getenv('PDF_PASSWORD')
PDF_PATH = 'pdf/3055_marzec_2026.pdf'
OPERATION_KEYWORDS = ['ZAKUPPRZYUŻYCIUKARTY', 
                      'PRZELEWWŁASNY',
                      'BLIKP2P-WYCHODZĄCY',
                      'AUTOMATYCZNASPŁATAKARTY',
                      'WYPŁATAWBANKOMACIE', 
                      'PROWIZJA',
                      'BLIKZAKUPE-COMMERCE',
                    ]

def get_lines(pdf) -> list[str]:
    all_lines = []

    for page in pdf.pages:
        text = page.extract_text()
        lines = text.splitlines()
        all_lines.extend(lines)

    return all_lines

def is_transaction_start(line: str, operation_keywords: list) -> bool:
    date_pattern = r"^\d{2}-\d{2}-\d{4}"
    return (bool(re.match(date_pattern, line)) 
            and any(keyword in line for keyword in operation_keywords))

def is_transaction_line(line: str) -> bool:
    pass


def group_lines_into_transactions(lines) -> list:
    transactions = []
    current_transaction = []

    for line in lines:
        if is_transaction_start(line, OPERATION_KEYWORDS):
            if current_transaction:
                transactions.append(current_transaction)
            current_transaction = [line]
        else:
            if current_transaction:
                current_transaction.append(line)            
    return transactions


def main():

    with pdfplumber.open(PDF_PATH, password=PDF_PASSWORD) as pdf:
        
        lines = get_lines(pdf)

        transactions = group_lines_into_transactions(lines)
        pprint(transactions, width=100, indent=2)     


if __name__ == "__main__":
    main()