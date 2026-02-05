import { useState } from "react";
import type { ImportResult } from "../api/transactions";
import { importTransactions } from "../api/transactions";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const importResult = await importTransactions(file);
      setResult(importResult);
      setFile(null);
      // Reset file input
      const fileInput = document.getElementById("file-input") as HTMLInputElement;
      if (fileInput) fileInput.value = "";
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to import transactions");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1>Import Transactions</h1>

      <form onSubmit={handleUpload} style={{ marginBottom: 24 }}>
        <div style={{ marginBottom: 16 }}>
          <label htmlFor="file-input" style={{ display: "block", marginBottom: 8 }}>
            Select CSV file:
          </label>
          <input
            id="file-input"
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            style={{ padding: 8 }}
          />
        </div>
        <button type="submit" disabled={!file || loading} style={{ padding: "8px 16px" }}>
          {loading ? "Uploading..." : "Upload"}
        </button>
      </form>

      {error && (
        <div
          role="alert"
          style={{
            padding: 16,
            backgroundColor: "#fee",
            border: "1px solid #fcc",
            borderRadius: 4,
            color: "#c00",
            marginBottom: 16,
          }}
        >
          {error}
        </div>
      )}

      {result && (
        <div
          style={{
            padding: 16,
            backgroundColor: "#efe",
            border: "1px solid #cfc",
            borderRadius: 4,
            marginBottom: 16,
          }}
        >
          <h2>Import Successful!</h2>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li>
              <strong>Imported:</strong> {result.imported} transactions
            </li>
            <li>
              <strong>Skipped:</strong> {result.skipped} duplicates
            </li>
            <li>
              <strong>Accounts created:</strong> {result.accounts_created}
            </li>
            <li>
              <strong>Categories created:</strong> {result.categories_created}
            </li>
          </ul>
        </div>
      )}

      <div
        style={{
          padding: 16,
          backgroundColor: "#f5f5f5",
          border: "1px solid #ddd",
          borderRadius: 4,
        }}
      >
        <h3>CSV Format</h3>
        <p>Your CSV file should have the following columns:</p>
        <ul>
          <li>
            <code>date</code> — Transaction date (YYYY-MM-DD)
          </li>
          <li>
            <code>description</code> — Transaction description
          </li>
          <li>
            <code>amount</code> — Amount (negative for expenses, positive for income)
          </li>
          <li>
            <code>account</code> — Account name (optional)
          </li>
          <li>
            <code>category</code> — Category name (optional)
          </li>
        </ul>
      </div>
    </div>
  );
}
