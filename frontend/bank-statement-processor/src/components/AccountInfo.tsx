import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface AccountInfoProps {
  uuid: string;
}

const AccountInfo: React.FC<AccountInfoProps> = ({ uuid }) => {
  const [accountInfo, setAccountInfo] = useState<any>(null);

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

  return (
    <div>
      <h2>Account Information</h2>
      <p><strong>Name:</strong> {accountInfo.name}</p>
      <p><strong>Address:</strong> {accountInfo.address}</p>
      <p><strong>Account Number:</strong> {accountInfo.account.number}</p>
      <p><strong>Statement Date:</strong> {accountInfo.account.statement_date}</p>
      <p><strong>Balance:</strong> {accountInfo.account.balance}</p>
    </div>
  );
};

export default AccountInfo;
