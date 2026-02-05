import { useCallback, useEffect, useState } from "react";
import type {
  DashboardSummary,
  SpendingByCategoryResponse,
  IncomeVsExpensesResponse,
  RecurringChargesResponse,
} from "../api/dashboard";
import {
  getDashboardSummary,
  getSpendingByCategory,
  getIncomeVsExpenses,
  getRecurringCharges,
} from "../api/dashboard";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [spending, setSpending] = useState<SpendingByCategoryResponse | null>(null);
  const [incomeVsExpenses, setIncomeVsExpenses] = useState<IncomeVsExpensesResponse | null>(null);
  const [recurring, setRecurring] = useState<RecurringChargesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatCurrency = (amount: number) => {
    return `$${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
  };

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [summaryData, spendingData, incomeData, recurringData] = await Promise.all([
        getDashboardSummary(),
        getSpendingByCategory(),
        getIncomeVsExpenses(),
        getRecurringCharges(),
      ]);
      setSummary(summaryData);
      setSpending(spendingData);
      setIncomeVsExpenses(incomeData);
      setRecurring(recurringData);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch dashboard data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 20 }}>
      <h1>Dashboard</h1>

      {error && (
        <p role="alert" style={{ color: "red" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading...</p>}

      {summary && (
        <>
          {/* Summary Cards */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: 16,
              marginBottom: 32,
            }}
          >
            <div style={{ padding: 16, border: "1px solid #ddd", borderRadius: 4 }}>
              <div style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>Total Income</div>
              <div style={{ fontSize: 24, fontWeight: "bold", color: "green" }}>
                {formatCurrency(summary.total_income)}
              </div>
            </div>
            <div style={{ padding: 16, border: "1px solid #ddd", borderRadius: 4 }}>
              <div style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>Total Expenses</div>
              <div style={{ fontSize: 24, fontWeight: "bold", color: "red" }}>
                {formatCurrency(summary.total_expenses)}
              </div>
            </div>
            <div style={{ padding: 16, border: "1px solid #ddd", borderRadius: 4 }}>
              <div style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>Net Savings</div>
              <div
                style={{
                  fontSize: 24,
                  fontWeight: "bold",
                  color: summary.net_savings >= 0 ? "green" : "red",
                }}
              >
                {summary.net_savings >= 0 ? "" : "-"}
                {formatCurrency(summary.net_savings)}
              </div>
            </div>
            <div style={{ padding: 16, border: "1px solid #ddd", borderRadius: 4 }}>
              <div style={{ fontSize: 14, color: "#666", marginBottom: 8 }}>Savings Rate</div>
              <div style={{ fontSize: 24, fontWeight: "bold" }}>
                {summary.savings_rate.toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Stats */}
          <div style={{ marginBottom: 32 }}>
            <p>
              <strong>{summary.transaction_count}</strong> transactions across{" "}
              <strong>{summary.account_count}</strong> accounts
            </p>
          </div>
        </>
      )}

      {/* Top Spending Categories */}
      {spending && spending.items.length > 0 && (
        <div style={{ marginBottom: 32 }}>
          <h2>Top Spending Categories</h2>
          <div style={{ border: "1px solid #ddd", borderRadius: 4 }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ backgroundColor: "#f5f5f5" }}>
                  <th style={{ padding: 12, textAlign: "left" }}>Category</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Amount</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Transactions</th>
                  <th style={{ padding: 12, textAlign: "right" }}>% of Total</th>
                </tr>
              </thead>
              <tbody>
                {spending.items.map((cat, idx) => (
                  <tr key={idx} style={{ borderTop: "1px solid #eee" }}>
                    <td style={{ padding: 12 }}>{cat.category_name}</td>
                    <td style={{ padding: 12, textAlign: "right", color: "red" }}>
                      {formatCurrency(cat.total)}
                    </td>
                    <td style={{ padding: 12, textAlign: "right" }}>{cat.transaction_count}</td>
                    <td style={{ padding: 12, textAlign: "right" }}>
                      {cat.percentage.toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Monthly Income vs Expenses */}
      {incomeVsExpenses && incomeVsExpenses.items.length > 0 && (
        <div style={{ marginBottom: 32 }}>
          <h2>Monthly Income vs Expenses</h2>
          <div style={{ border: "1px solid #ddd", borderRadius: 4 }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ backgroundColor: "#f5f5f5" }}>
                  <th style={{ padding: 12, textAlign: "left" }}>Month</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Income</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Expenses</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Net</th>
                </tr>
              </thead>
              <tbody>
                {incomeVsExpenses.items.map((month, idx) => (
                  <tr key={idx} style={{ borderTop: "1px solid #eee" }}>
                    <td style={{ padding: 12 }}>{month.month}</td>
                    <td style={{ padding: 12, textAlign: "right", color: "green" }}>
                      {formatCurrency(month.income)}
                    </td>
                    <td style={{ padding: 12, textAlign: "right", color: "red" }}>
                      {formatCurrency(month.expenses)}
                    </td>
                    <td
                      style={{
                        padding: 12,
                        textAlign: "right",
                        color: month.net >= 0 ? "green" : "red",
                      }}
                    >
                      {month.net >= 0 ? "" : "-"}
                      {formatCurrency(month.net)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recurring Charges */}
      {recurring && recurring.items.length > 0 && (
        <div style={{ marginBottom: 32 }}>
          <h2>Recurring Charges</h2>
          <p>
            Total Monthly Recurring:{" "}
            <strong>{formatCurrency(recurring.total_monthly_recurring)}</strong>
          </p>
          <div style={{ border: "1px solid #ddd", borderRadius: 4 }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ backgroundColor: "#f5f5f5" }}>
                  <th style={{ padding: 12, textAlign: "left" }}>Description</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Average Amount</th>
                  <th style={{ padding: 12, textAlign: "left" }}>Frequency</th>
                  <th style={{ padding: 12, textAlign: "right" }}>Occurrences</th>
                  <th style={{ padding: 12, textAlign: "left" }}>Category</th>
                </tr>
              </thead>
              <tbody>
                {recurring.items.map((charge, idx) => (
                  <tr key={idx} style={{ borderTop: "1px solid #eee" }}>
                    <td style={{ padding: 12 }}>{charge.description}</td>
                    <td style={{ padding: 12, textAlign: "right", color: "red" }}>
                      {formatCurrency(charge.average_amount)}
                    </td>
                    <td style={{ padding: 12 }}>{charge.frequency}</td>
                    <td style={{ padding: 12, textAlign: "right" }}>{charge.occurrences}</td>
                    <td style={{ padding: 12 }}>{charge.category_name || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
