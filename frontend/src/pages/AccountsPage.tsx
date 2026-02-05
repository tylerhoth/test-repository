import { useCallback, useEffect, useState } from "react";
import type { Account, AccountListResponse } from "../api/accounts";
import { listAccounts } from "../api/accounts";

export default function AccountsPage() {
  const [data, setData] = useState<AccountListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAccounts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listAccounts({ page_size: 1000 });
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch accounts");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  return (
    <div style={{ maxWidth: 1000, margin: "0 auto", padding: 20 }}>
      <h1>Accounts</h1>

      {error && (
        <p role="alert" style={{ color: "red" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading...</p>}

      {data && (
        <>
          <p>{data.total} account(s)</p>

          {data.items.length > 0 ? (
            <div style={{ border: "1px solid #ddd", borderRadius: 4 }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ backgroundColor: "#f5f5f5" }}>
                    <th style={{ padding: 12, textAlign: "left" }}>Name</th>
                    <th style={{ padding: 12, textAlign: "left" }}>Institution</th>
                    <th style={{ padding: 12, textAlign: "left" }}>Type</th>
                    <th style={{ padding: 12, textAlign: "left" }}>Last Four</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((account: Account) => (
                    <tr key={account.id} style={{ borderTop: "1px solid #eee" }}>
                      <td style={{ padding: 12, fontWeight: "bold" }}>{account.name}</td>
                      <td style={{ padding: 12 }}>{account.institution}</td>
                      <td style={{ padding: 12 }}>{account.account_type}</td>
                      <td style={{ padding: 12 }}>{account.last_four || "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No accounts found. Import transactions to create accounts automatically.</p>
          )}
        </>
      )}
    </div>
  );
}
