import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import AccountInfo from './components/AccountInfo';
import TransactionsTable from './components/TransactionsTable';

interface UploadedDocument {
  uuid: string;
  name: string;
}

const App: React.FC = () => {
  const [uploadedDocuments, setUploadedDocuments] = useState<UploadedDocument[]>([]);
  const [selectedUuid, setSelectedUuid] = useState<string | null>(null);

  // Load documents from localStorage on component mount
  useEffect(() => {
    const savedDocuments = localStorage.getItem('uploadedDocuments');
    if (savedDocuments) {
      setUploadedDocuments(JSON.parse(savedDocuments));
    }
  }, []);

  // Save documents to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('uploadedDocuments', JSON.stringify(uploadedDocuments));
  }, [uploadedDocuments]);

  const handleUploadSuccess = (uuid: string, name: string) => {
    const newDocument = { uuid, name };
    setUploadedDocuments((prev) => [...prev, newDocument]);
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
          <FileUpload onUploadSuccess={handleUploadSuccess} />
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
