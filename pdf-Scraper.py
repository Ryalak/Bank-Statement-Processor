import pdfplumber
import re

def extract_account_info(text):
    """
    Extracts account information from the text.
    """
    account_info = {}

    # Patterns to match account details
    account_holder_match = re.search(r"Account Holder:\s*(.+)", text)
    account_name_match = re.search(r"Account Name:\s*(.+)", text)
    account_number_match = re.search(r"Account Number:\s*(\d+)", text)
    address_match = re.search(r"Address:\s*(.+)", text)
    statement_date_match = re.search(r"Statement Date:\s*(.+)", text)

    # Assign matches to the dictionary if they exist
    if account_holder_match:
        account_info['account_holder'] = account_holder_match.group(1)
    if account_name_match:
        account_info['account_name'] = account_name_match.group(1)
    if account_number_match:
        account_info['account_number'] = account_number_match.group(1)
    if address_match:
        account_info['address'] = address_match.group(1)
    if statement_date_match:
        account_info['statement_date'] = statement_date_match.group(1)

    return account_info

def extract_transactions(text):
    """
    Extracts transactions from the text, handling various spacing and newline inconsistencies.
    """
    transactions = []

    # Revised pattern to be more lenient with whitespace
    transaction_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2})\s+(.+?)\s+(\d+\.\d+)?\s+(\d+\.\d+)?(?:\s+\d+\.\d+)?",
        re.DOTALL  # Allows matching across newlines
    )

    # Split by lines to handle each transaction individually
    lines = text.split("\n")
    for line in lines:
        match = transaction_pattern.search(line)
        if match:
            date = match.group(1)
            description = match.group(2).strip()
            credit = match.group(3) if match.group(3) else None
            debit = match.group(4) if match.group(4) else None

            transactions.append({
                'date': date,
                'description': description,
                'credit': float(credit) if credit else None,
                'debit': float(debit) if debit else None
            })

    return transactions

def parse_pdf(file_path):
    """
    Parses the PDF and extracts account information and transactions.
    """
    account_info = {}
    transactions = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Extract account info and transactions from the page
                if not account_info:  # Only attempt to extract account info once
                    account_info = extract_account_info(text)
                transactions.extend(extract_transactions(text))
    
    return account_info, transactions

# Example usage
file_path = './files/1.pdf'
account_info, transactions = parse_pdf(file_path)

# Display the extracted information
print("Account Information:", account_info)
print("Transactions:")
for transaction in transactions:
    print(transaction)
