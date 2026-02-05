import { api } from "./client";

export interface Budget {
  id: number;
  category_id: number;
  amount_limit: number;
  created_at: string;
}

export interface BudgetListResponse {
  items: Budget[];
  total: number;
  page: number;
  page_size: number;
}

export function listBudgets(): Promise<BudgetListResponse> {
  return api.get<BudgetListResponse>("/api/budgets");
}

export function createBudget(data: { category_id: number; amount_limit: number }): Promise<Budget> {
  return api.post<Budget>("/api/budgets", data);
}

export function deleteBudget(id: number): Promise<void> {
  return api.delete<void>(`/api/budgets/${id}`);
}
