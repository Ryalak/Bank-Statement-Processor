import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import AccountInfo from './components/AccountInfo';
import TransactionsTable from './components/TransactionsTable';

const App: React.FC = () => {
  const [uuid, setUuid] = useState<string | null>(null);

  return (
    <div style={{ paddingLeft: '10px' }}>
      <h1>Bank Statement Processor</h1>
      {!uuid && <FileUpload onUploadSuccess={setUuid} />}
      {uuid && <AccountInfo uuid={uuid} />}
      {uuid && <TransactionsTable uuid={uuid} />}
    </div>
  );
};

export default App;
