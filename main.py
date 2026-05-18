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
                      'OPŁATA',
                      'PRZYCHODZĄCY',
                    ]
DATE_PATTERN = r"^\d{2}-\d{2}-\d{4}"

def get_lines(pdf) -> list[str]:
    all_lines = []

    for page in pdf.pages:
        text = page.extract_text()
        lines = text.splitlines()
        all_lines.extend(lines)

    return all_lines

def is_transaction_start(line: str, operation_keywords: list) -> bool:
    return (bool(re.match(DATE_PATTERN, line)) 
            and any(keyword in line for keyword in operation_keywords))

def is_transaction_line(line: str) -> bool:
    if is_transaction_start(line, OPERATION_KEYWORDS):
        return True
    elif "DATATRANSAKCJI" in line or "PLN" in line:
        return True
    else:
        return False
    


def group_lines_into_transactions(lines) -> list:
    transactions = []
    current_transaction = []

    for line in lines:
        if is_transaction_start(line, OPERATION_KEYWORDS):
            if current_transaction:
                transactions.append(current_transaction)
            current_transaction = [line]
        else:
            if current_transaction and is_transaction_line(line):
                current_transaction.append(line)
    if current_transaction:
        transactions.append(current_transaction)
    return transactions

def parse_transaction_block(block: list[str]) -> dict:
    first_line = block[0]
    transaction_details: dict[str, str | None] = {
        "date": None ,
        "operation_type": None,
        "amount": None,
    }
    match = re.search(DATE_PATTERN, first_line)
    if match:
        transaction_details["date"] = match.group()

    return transaction_details




def main():

    with pdfplumber.open(PDF_PATH, password=PDF_PASSWORD) as pdf:
        
        lines = get_lines(pdf)

        transactions = group_lines_into_transactions(lines)
        for transaction in transactions:
            parsed = parse_transaction_block(transaction)
            print(parsed)
         


if __name__ == "__main__":
    main()