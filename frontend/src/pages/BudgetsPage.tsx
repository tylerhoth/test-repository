import { useCallback, useEffect, useState } from "react";
import type { Budget, BudgetListResponse } from "../api/budgets";
import { listBudgets, createBudget, deleteBudget } from "../api/budgets";
import type { Category, CategoryListResponse } from "../api/categories";
import { listCategories } from "../api/categories";

export default function BudgetsPage() {
  const [budgets, setBudgets] = useState<BudgetListResponse | null>(null);
  const [categories, setCategories] = useState<CategoryListResponse | null>(null);
  const [selectedCategoryId, setSelectedCategoryId] = useState<number | "">("");
  const [amountLimit, setAmountLimit] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatCurrency = (amount: number) => {
    return `$${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
  };

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [budgetsData, categoriesData] = await Promise.all([
        listBudgets(),
        listCategories({ page_size: 1000 }),
      ]);
      setBudgets(budgetsData);
      setCategories(categoriesData);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCategoryId || !amountLimit) return;

    try {
      await createBudget({
        category_id: Number(selectedCategoryId),
        amount_limit: parseFloat(amountLimit),
      });
      setSelectedCategoryId("");
      setAmountLimit("");
      await fetchData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create budget");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteBudget(id);
      await fetchData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete budget");
    }
  };

  const getCategoryName = (categoryId: number): string => {
    const category = categories?.items.find((c) => c.id === categoryId);
    return category?.name || `Category ${categoryId}`;
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1>Budgets</h1>

      {/* Create Budget Form */}
      <div
        style={{
          padding: 16,
          border: "1px solid #ddd",
          borderRadius: 4,
          marginBottom: 24,
          backgroundColor: "#f9f9f9",
        }}
      >
        <h2>Create New Budget</h2>
        <form onSubmit={handleCreate} style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <select
            value={selectedCategoryId}
            onChange={(e) => setSelectedCategoryId(e.target.value ? Number(e.target.value) : "")}
            aria-label="Select category"
            style={{ flex: 1, minWidth: 200, padding: 8 }}
          >
            <option value="">Select category...</option>
            {categories?.items.map((cat: Category) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
          <input
            type="number"
            step="0.01"
            value={amountLimit}
            onChange={(e) => setAmountLimit(e.target.value)}
            placeholder="Amount limit"
            aria-label="Amount limit"
            style={{ width: 150, padding: 8 }}
          />
          <button type="submit" disabled={!selectedCategoryId || !amountLimit}>
            Create Budget
          </button>
        </form>
      </div>

      {error && (
        <p role="alert" style={{ color: "red" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading...</p>}

      {budgets && (
        <>
          <p>{budgets.total} budget(s)</p>

          {budgets.items.length > 0 ? (
            <div style={{ border: "1px solid #ddd", borderRadius: 4 }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ backgroundColor: "#f5f5f5" }}>
                    <th style={{ padding: 12, textAlign: "left" }}>Category</th>
                    <th style={{ padding: 12, textAlign: "right" }}>Limit</th>
                    <th style={{ padding: 12, textAlign: "center" }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {budgets.items.map((budget: Budget) => (
                    <tr key={budget.id} style={{ borderTop: "1px solid #eee" }}>
                      <td style={{ padding: 12 }}>{getCategoryName(budget.category_id)}</td>
                      <td style={{ padding: 12, textAlign: "right", fontWeight: "bold" }}>
                        {formatCurrency(budget.amount_limit)}
                      </td>
                      <td style={{ padding: 12, textAlign: "center" }}>
                        <button
                          onClick={() => handleDelete(budget.id)}
                          aria-label={`Delete budget for ${getCategoryName(budget.category_id)}`}
                          style={{ padding: "4px 8px" }}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No budgets created yet.</p>
          )}
        </>
      )}
    </div>
  );
}
