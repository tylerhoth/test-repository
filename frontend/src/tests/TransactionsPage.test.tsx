import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import TransactionsPage from "../pages/TransactionsPage";

const mockListTransactions = vi.fn();

vi.mock("../api/transactions", () => ({
  listTransactions: (...args: unknown[]) => mockListTransactions(...args),
  importTransactions: vi.fn(),
}));

describe("TransactionsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockListTransactions.mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
    });
  });

  it("renders the heading", async () => {
    render(<TransactionsPage />);
    expect(screen.getByRole("heading", { name: /transactions/i })).toBeInTheDocument();
    await waitFor(() => expect(mockListTransactions).toHaveBeenCalled());
  });

  it("displays transactions from the API", async () => {
    mockListTransactions.mockResolvedValue({
      items: [
        {
          id: 1,
          date: "2026-01-15",
          description: "Grocery Store",
          amount: -45.67,
          category_id: 1,
          account_id: 1,
          is_recurring: false,
          raw_description: null,
          tags: null,
          notes: null,
          created_at: "2026-01-15T00:00:00",
        },
        {
          id: 2,
          date: "2026-01-15",
          description: "Payroll",
          amount: 5700,
          category_id: 2,
          account_id: 1,
          is_recurring: false,
          raw_description: null,
          tags: null,
          notes: null,
          created_at: "2026-01-15T00:00:00",
        },
      ],
      total: 2,
      page: 1,
      page_size: 20,
    });

    render(<TransactionsPage />);
    await waitFor(() => {
      expect(screen.getByText("Grocery Store")).toBeInTheDocument();
      expect(screen.getByText("Payroll")).toBeInTheDocument();
    });
    expect(screen.getByText(/2 transaction\(s\)/)).toBeInTheDocument();
  });

  it("handles search", async () => {
    const user = userEvent.setup();
    render(<TransactionsPage />);
    await waitFor(() => expect(mockListTransactions).toHaveBeenCalled());

    const input = screen.getByLabelText("Search transactions");
    await user.type(input, "Grocery");
    await user.click(screen.getByRole("button", { name: /search/i }));

    expect(mockListTransactions).toHaveBeenCalledWith(expect.objectContaining({ q: "Grocery" }));
  });

  it("shows error on fetch failure", async () => {
    mockListTransactions.mockRejectedValue(new Error("Network error"));
    render(<TransactionsPage />);
    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Network error");
    });
  });
});
