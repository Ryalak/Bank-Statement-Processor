import pdfplumber
import re

def extract_account_info(text):
    """
    Extracts account information from the text.
    """
    account_info = {}

    # Patterns to match account details using regex patterns
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

    # transaction regex pattern
    transaction_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2})\s+(.+?)\s+(\d+\.\d+)?\s+([A-Za-z]?\d+\.\d+)?(?:\s+\d+\.\d+)?",
        re.DOTALL 
    )
    
    # Regex pattern to check if there will be no more tranactions 
    final_pattern_check = re.compile(
        r"Transactions not yet processed on your account:"
    )

    # Split by lines to handle each transaction individually
    lines = text.split("\n")
    previous_balance = 0.0 # Used to determine whether an amount is Debit or Credit
    last_transaction_check = False
    
    for line in lines:
        match = transaction_pattern.search(line) # Match transaction pattern to line
        if match:
            # Extract different components of transaction
            date = match.group(1)
            description = match.group(2).strip()
            amount = match.group(3) 
            balance = match.group(4)

            # A check used in case of invisible currency characters 
            if not balance.replace('.', '', 1).isdigit():
                balance = balance[1:]

            # Add transactions to an array
            transactions.append({
                'date': date,
                'description': description.strip("-"),
                'amount': float(amount) if amount else None,
                'type': "Debit" if float(balance) < previous_balance else "Credit",
                'balance': float(balance) if balance else None
            })

            previous_balance = float(balance)
            last_transaction_check = True
        
        # Used to flag final transaction
        elif final_pattern_check.search(line):
            last_transaction_check = False

        # Used for multi-line descriptions
        elif last_transaction_check:
            transactions[-1]['description'] += line
            last_transaction_check = False

    return transactions

def parse_pdf(file_path):
    """
    Parses the PDF and extracts account information and transactions.
    """
    account_info = {}
    transactions = []
    
    with pdfplumber.open(file_path) as pdf: # Open file with pdfplumber and extract the text on each page
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Extract account info and transactions from the page
                if not account_info:  # Only attempt to extract account info once
                    account_info = extract_account_info(text)
                transactions.extend(extract_transactions(text))
    
    return account_info, transactions
