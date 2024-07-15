import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [individualSummaries, setIndividualSummaries] = useState([]);
  const [overallSummary, setOverallSummary] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSummarize = async () => {
    if (!file) {
      alert('Please upload a CSV file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/summarize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setIndividualSummaries(response.data.individual_summaries);
      setOverallSummary(response.data.overall_summary);
      setDownloadUrl(`http://localhost:5000/${response.data.download_url}`);
    } catch (error) {
      console.error('Error summarizing feedback:', error);
    }
  };

  return (
    <div className="App">
      <h1>Customer Feedback Analysis</h1>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <br />
      <button onClick={handleSummarize}>Summarize Feedback</button>
      {downloadUrl && (
        <div>
          <h2>Download Summaries</h2>
          <a href={downloadUrl} download>Download CSV</a>
        </div>
      )}
      <div>
        <h2>Individual Summaries</h2>
        {individualSummaries.map((summary, index) => (
          <p key={index}><strong>Summary {index + 1}:</strong> {summary}</p>
        ))}
      </div>
      {overallSummary && (
        <div>
          <h2>Overall Summary:</h2>
          <p>{overallSummary}</p>
        </div>
      )}
    </div>
  );
}

export default App;
