import pdfplumber
import sqlite3
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

    transaction_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2})\s+(.+?)\s+(\d+\.\d+)?\s+(\d+\.\d+)?(?:\s+\d+\.\d+)?",
        re.DOTALL 
    )

    # Split by lines to handle each transaction individually
    lines = text.split("\n")
    for line in lines:
        match = transaction_pattern.search(line)
        if match:
            date = match.group(1)
            description = match.group(2).strip()
            credit_or_debit = match.group(3) if match.group(3) else None
            balance = match.group(4) if match.group(4) else None

            transactions.append({
                'date': date,
                'description': description,
                'credit_or_debit': float(credit_or_debit) if credit_or_debit else None,
                'balance': float(balance) if balance else None
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

def initialize_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Account table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_holder TEXT,
            account_name TEXT,
            account_number TEXT,
            address TEXT,
            statement_date TEXT
        )
    ''')

    # Create Transaction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS [Transaction] (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            date TEXT,
            description TEXT,
            credit_or_debit REAL,
            balance REAL,
            FOREIGN KEY (account_id) REFERENCES Account(account_id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_account(account_info, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert into Account table
    cursor.execute('''
        INSERT INTO Account (account_holder, account_name, account_number, address, statement_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        account_info['account_holder'],
        account_info['account_name'],
        account_info['account_number'],
        account_info['address'],
        account_info['statement_date']
    ))

    # Get the inserted account_id
    account_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return account_id

def insert_transactions(account_id, transactions, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert each transaction linked to the account_id
    for transaction in transactions:
        cursor.execute('''
            INSERT INTO [Transaction] (account_id, date, description, credit_or_debit, balance)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            account_id,
            transaction['date'],
            transaction['description'],
            transaction['credit_or_debit'],
            transaction['balance']
        ))

    conn.commit()
    conn.close()

def get_account(account_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Account WHERE account_id = ?', (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account

def get_transactions(account_id, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM [Transaction] WHERE account_id = ?', (account_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def main():
    file_path = './files/1.pdf'
    account_info, transactions = parse_pdf(file_path)

    db_name = "bank_statements.db"
    initialize_database(db_name)

    account_id = insert_account(account_info, db_name)
    insert_transactions(account_id, transactions, db_name)

    print("Data has been successfully saved to the database.")

    print(get_account(account_id, db_name))

    print(get_transactions(account_id, db_name))

if __name__=="__main__":
    main()



