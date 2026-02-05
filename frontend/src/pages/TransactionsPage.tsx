import { useCallback, useEffect, useState } from "react";
import type { Transaction, TransactionListResponse } from "../api/transactions";
import { listTransactions } from "../api/transactions";

export default function TransactionsPage() {
  const [data, setData] = useState<TransactionListResponse | null>(null);
  const [search, setSearch] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatCurrency = (amount: number) => {
    return `$${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
  };

  const fetchTransactions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listTransactions({
        page: currentPage,
        page_size: 20,
        q: search || undefined,
        sort_by: "date",
        sort_dir: "desc",
      });
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch transactions");
    } finally {
      setLoading(false);
    }
  }, [currentPage, search]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchTransactions();
  };

  const totalPages = data ? Math.ceil(data.total / data.page_size) : 0;

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 20 }}>
      <h1>Transactions</h1>

      <form onSubmit={handleSearch} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search transactions..."
          aria-label="Search transactions"
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit">Search</button>
      </form>

      {error && (
        <p role="alert" style={{ color: "red" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading...</p>}

      {data && (
        <>
          <p>
            {data.total} transaction(s) — Page {data.page} of {totalPages}
          </p>

          <div style={{ border: "1px solid #ddd", borderRadius: 4, marginBottom: 16 }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ backgroundColor: "#f5f5f5" }}>
                  <th style={{ padding: 12, textAlign: "left" }}>Date</th>
                  <th style={{ padding: 12, textAlign: "left" }}>Description</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Amount</th>
                  <th style={{ padding: 12, textAlign: "left" }}>Category</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((transaction: Transaction) => (
                  <tr key={transaction.id} style={{ borderTop: "1px solid #eee" }}>
                    <td style={{ padding: 12 }}>{transaction.date}</td>
                    <td style={{ padding: 12 }}>{transaction.description}</td>
                    <td
                      style={{
                        padding: 12,
                        textAlign: "right",
                        color: transaction.amount >= 0 ? "green" : "red",
                        fontWeight: "bold",
                      }}
                    >
                      {transaction.amount >= 0 ? "" : "-"}
                      {formatCurrency(transaction.amount)}
                    </td>
                    <td style={{ padding: 12 }}>
                      {transaction.category_id ? `Category ${transaction.category_id}` : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div style={{ display: "flex", gap: 8, justifyContent: "center", alignItems: "center" }}>
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              style={{ padding: "8px 16px" }}
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              style={{ padding: "8px 16px" }}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}
