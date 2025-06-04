import React, { useState } from 'react';
import './index.css'; // ensure Tailwind styles are loaded

function App() {
  const [output, setOutput] = useState('No results yet.');

  async function runAgent() {
    setOutput("Running agent... please wait.");
    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: "backend/sample.py" }),
      });
      const data = await response.json();
      setOutput(data.suggestions);
    } catch (err) {
      setOutput("Error calling agent: " + err.toString());
    }
  }

  async function createTests() {
    setOutput("Generating tests... please wait.");
    try {
      const response = await fetch("http://127.0.0.1:8000/generate-test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: "backend/sample.py" }),
      });
      const data = await response.json();
      setOutput(data.result);
    } catch (err) {
      setOutput("Error generating tests: " + err.toString());
    }
  }

  async function updateDocs() {
    setOutput("Updating documentation... please wait.");
    try {
      const response = await fetch("http://127.0.0.1:8000/update-docs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: "backend/sample.py" }),
      });
      const data = await response.json();
      setOutput(data.result);
    } catch (err) {
      setOutput("Error updating docs: " + err.toString());
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-6 space-y-4">
        <h1 className="text-2xl font-bold">AI Developer Productivity Agent</h1>

        <div className="space-x-2">
          <button
            onClick={runAgent}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
          >
            Run Agent on sample.py
          </button>
          <button
            onClick={createTests}
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded"
          >
            Generate Tests
          </button>
          <button
            onClick={updateDocs}
            className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded"
          >
            Update Documentation
          </button>
        </div>

        <div className="p-4 bg-gray-50 rounded">
          <h2 className="font-semibold mb-2">Agent Output:</h2>
          <pre className="whitespace-pre-wrap">{output}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
