import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import DashboardPage from "../pages/DashboardPage";

const mockGetSummary = vi.fn();
const mockGetSpending = vi.fn();
const mockGetIncomeVsExpenses = vi.fn();
const mockGetRecurring = vi.fn();

vi.mock("../api/dashboard", () => ({
  getDashboardSummary: (...args: unknown[]) => mockGetSummary(...args),
  getSpendingByCategory: (...args: unknown[]) => mockGetSpending(...args),
  getIncomeVsExpenses: (...args: unknown[]) => mockGetIncomeVsExpenses(...args),
  getRecurringCharges: (...args: unknown[]) => mockGetRecurring(...args),
}));

describe("DashboardPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetSummary.mockResolvedValue({
      total_income: 10000,
      total_expenses: 7000,
      net_savings: 3000,
      savings_rate: 30.0,
      transaction_count: 100,
      account_count: 5,
    });
    mockGetSpending.mockResolvedValue({ items: [], total_expenses: 0 });
    mockGetIncomeVsExpenses.mockResolvedValue({ items: [] });
    mockGetRecurring.mockResolvedValue({ items: [], total_monthly_recurring: 0 });
  });

  it("renders the heading", async () => {
    render(<DashboardPage />);
    expect(screen.getByRole("heading", { name: /dashboard/i })).toBeInTheDocument();
    await waitFor(() => expect(mockGetSummary).toHaveBeenCalled());
  });

  it("displays summary data", async () => {
    render(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("$10,000.00")).toBeInTheDocument();
      expect(screen.getByText("$7,000.00")).toBeInTheDocument();
      expect(screen.getByText("$3,000.00")).toBeInTheDocument();
      expect(screen.getByText("30.0%")).toBeInTheDocument();
    });
  });

  it("displays transaction and account counts", async () => {
    render(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
      expect(screen.getByText("5")).toBeInTheDocument();
    });
  });

  it("shows error on fetch failure", async () => {
    mockGetSummary.mockRejectedValue(new Error("Network error"));
    render(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Network error");
    });
  });

  it("displays spending categories", async () => {
    mockGetSpending.mockResolvedValue({
      items: [
        {
          category_id: 1,
          category_name: "Restaurants",
          total: 500,
          transaction_count: 20,
          percentage: 25.0,
        },
      ],
      total_expenses: 2000,
    });
    render(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("Restaurants")).toBeInTheDocument();
      expect(screen.getByText("$500.00")).toBeInTheDocument();
    });
  });
});
