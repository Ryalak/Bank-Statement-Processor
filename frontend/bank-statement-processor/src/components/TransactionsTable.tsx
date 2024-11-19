import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "../App.css";

interface TransactionsTableProps {
  uuid: string;
}

const TransactionsTable: React.FC<TransactionsTableProps> = ({ uuid }) => {
  const [transactions, setTransactions] = useState<any[]>([]);

  // Await /transaction API endpoint and set data
  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/transactions?uuid=${uuid}`);
        setTransactions(response.data.data);
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    };

    fetchTransactions();
  }, [uuid]);

  if (transactions.length === 0) {
    return <div>Loading transactions...</div>;
  }

  // Display all information in a table 
  return (
    <div style={{ paddingLeft: '20px', paddingRight: '20px' }}>
      <h2>Transactions</h2>
      <table className='transactions-table'>
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Balance</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.uuid}>
              <td>{transaction.date}</td>
              <td>{transaction.description}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.balance}</td>
              <td>{transaction.type}</td>
            </tr>
          ))}
          <br />
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsTable;
