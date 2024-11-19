import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface AccountInfoProps {
  uuid: string;
}

const AccountInfo: React.FC<AccountInfoProps> = ({ uuid }) => {
  const [accountInfo, setAccountInfo] = useState<any>(null);

  // Await API requests
  useEffect(() => {
    const fetchAccountInfo = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/account?uuid=${uuid}`);
        setAccountInfo(response.data.data);
      } catch (error) {
        console.error('Error fetching account info:', error);
      }
    };

    fetchAccountInfo();
  }, [uuid]);

  if (!accountInfo) {
    return <div>Loading account info...</div>;
  }

  // Display all the data using accountInfo
  return (
    <div style={{ paddingLeft: '20px' }}>
      <h2>Account Information</h2>
      <p><strong>UUID:</strong> {accountInfo.account.uuid}</p>
      <p><strong>Name:</strong> {accountInfo.name}</p>
      <p><strong>Address:</strong> {accountInfo.address}</p>
      <p><strong>Account Number:</strong> {accountInfo.account.number}</p>
      <p><strong>Statement Date:</strong> {accountInfo.account.statement_date}</p>
      <p><strong>Balance:</strong> {accountInfo.account.balance}</p>
      <p><strong>From Date:</strong> {accountInfo.account.from_date} </p>
      <p><strong>To Date:</strong> {accountInfo.account.to_date}</p>
      <p><strong>Transaction Count:</strong> {accountInfo.account.transaction_count}</p>
    </div>
  );
};

export default AccountInfo;
