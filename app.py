import os
import uuid
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from collections import OrderedDict

from pdf_Scraper import parse_pdf, extract_transactions, extract_account_info
from db import initialize_database, insert_account, insert_transactions, get_account, get_transactions

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/account', methods=['GET'])
def get_account():
    """
    API Endpoint: Retrieve account information by UUID.
    """
    # Get the UUID from the query parameters
    statement_uuid = request.args.get('uuid')

    if not statement_uuid:
        return jsonify({"error": "UUID is required"}), 400

    db_name = "bank_statements.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query the Account table by UUID
    cursor.execute('SELECT * FROM Account WHERE uuid = ?', (statement_uuid,))
    account = cursor.fetchone()

    cursor.execute('SELECT COUNT(*), MIN(date), MAX(date), MIN(balance), MAX(balance) FROM [Transaction] WHERE account_id = ?', (account[0],))
    transaction_summary = cursor.fetchone()

    transaction_count = transaction_summary[0] or 0
    from_date = transaction_summary[1] or ""
    to_date = transaction_summary[2] or ""
    opening_balance = transaction_summary[3] or 0.0
    closing_balance = transaction_summary[4] or 0.0

    conn.close()

    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Map account fields to a JSON response
    account_info = OrderedDict({
        "uuid": account[6],
        "message": "Success",
        "data": OrderedDict({
            "name": account[1],
            "address": account[4],
            "account": OrderedDict({
                "uuid": account[6],
                "number": account[3],
                "balance": closing_balance,
                "opening_balance": opening_balance,
                "closing_balance": closing_balance,
                "from_date": from_date,
                "to_date": to_date,
                "transaction_count": transaction_count,
                "statement_date": account[5]
            })
        })
    })

    return jsonify(account_info), 200

@app.route('/statement', methods=['POST'])
def upload_statement():
    """
    API Endpoint: Upload a bank statement file and process it.
    """
    if 'statement' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['statement']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Generate a unique identifier for this transaction
    statement_uuid = str(uuid.uuid4())

    process_statement(file_path, statement_uuid)

    return jsonify({
        "uuid": statement_uuid,
        "message": "Success"
    }), 200

def process_statement(file_path, statement_uuid):
    """
    Process the bank statement file (parse, extract data, save to DB).
    """
    print(f"Processing file: {file_path}")
    db_name = "bank_statements.db"

    initialize_database(db_name)

    account_info, transactions = parse_pdf(file_path)

    account_id = insert_account(account_info, db_name, statement_uuid)
    insert_transactions(account_id, transactions, db_name)

    print(f"Processed statement for account: {account_info['account_holder']}")


if __name__ == '__main__':
    app.run(debug=True)
