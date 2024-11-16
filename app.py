import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from pdf_Scraper import parse_pdf, extract_transactions, extract_account_info
from db import initialize_database, insert_account, insert_transactions, get_account, get_transactions

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    process_statement(file_path)

    return jsonify({
        "uuid": statement_uuid,
        "message": "Success"
    }), 200

def process_statement(file_path):
    """
    Process the bank statement file (parse, extract data, save to DB).
    """
    print(f"Processing file: {file_path}")
    db_name = "bank_statements.db"

    initialize_database(db_name)

    account_info, transactions = parse_pdf(file_path)

    account_id = insert_account(account_info, db_name)
    insert_transactions(account_id, transactions, db_name)

    print(f"Processed statement for account: {account_info['account_holder']}")


if __name__ == '__main__':
    app.run(debug=True)
