import React, { useState } from 'react';
import axios from 'axios';

interface FileUploadProps {
  onUploadSuccess: (uuid: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('statement', file);

    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/statement', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess(response.data.uuid);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Statement'}
      </button>
    </div>
  );
};

export default FileUpload;
