import sqlite3

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