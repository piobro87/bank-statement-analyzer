import pdfplumber
import re

def main():

    pdf_path = ""
    password = ""

    with pdfplumber.open(pdf_path, password=password) as pdf:
        
        text = pdf.pages[0].extract_text()
        lines = text.splitlines()
        for line in lines:
            print(repr(line))


if __name__ == "__main__":
    main()