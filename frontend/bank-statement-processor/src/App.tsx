import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import AccountInfo from './components/AccountInfo';
import TransactionsTable from './components/TransactionsTable';
import "./App.css";

interface UploadedDocument {
  uuid: string;
  name: string; // Filename
}

const App: React.FC = () => {
  const [uploadedDocuments, setUploadedDocuments] = useState<UploadedDocument[]>([]);
  const [selectedUuid, setSelectedUuid] = useState<string | null>(null);

  const handleUploadSuccess = (uuid: string, name: string) => {
    setUploadedDocuments((prev) => [...prev, { uuid, name }]);
    setSelectedUuid(uuid);
  };

  const handleGoBack = () => {
    setSelectedUuid(null);
  };

  return (
    <div style={{ paddingLeft: '10px' }}>
      <h1>Bank Statement Processor</h1>

      {!selectedUuid ? (
        <>
          <FileUpload onUploadSuccess={(uuid) => handleUploadSuccess(uuid, `Document ${uploadedDocuments.length + 1}`)} />
          <h2>Uploaded Documents</h2>
          <ul>
            {uploadedDocuments.map((doc) => (
              <li key={doc.uuid}>
                <button onClick={() => setSelectedUuid(doc.uuid)}>
                  {doc.name} (UUID: {doc.uuid})
                </button>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <>
          <button onClick={handleGoBack}>Back</button>
          <AccountInfo uuid={selectedUuid} />
          <TransactionsTable uuid={selectedUuid} />
        </>
      )}
    </div>
  );
};

export default App;
