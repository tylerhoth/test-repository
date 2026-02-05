import { api } from "./client";

export interface DashboardSummary {
  total_income: number;
  total_expenses: number;
  net_savings: number;
  savings_rate: number;
  transaction_count: number;
  account_count: number;
}

export interface CategorySpending {
  category_id: number | null;
  category_name: string;
  total: number;
  transaction_count: number;
  percentage: number;
}

export interface SpendingByCategoryResponse {
  items: CategorySpending[];
  total_expenses: number;
}

export interface MonthlyComparison {
  month: string;
  income: number;
  expenses: number;
  net: number;
}

export interface IncomeVsExpensesResponse {
  items: MonthlyComparison[];
}

export interface RecurringCharge {
  description: string;
  average_amount: number;
  frequency: string;
  occurrences: number;
  category_name: string | null;
}

export interface RecurringChargesResponse {
  items: RecurringCharge[];
  total_monthly_recurring: number;
}

export function getDashboardSummary(): Promise<DashboardSummary> {
  return api.get<DashboardSummary>("/api/dashboard/summary");
}

export function getSpendingByCategory(): Promise<SpendingByCategoryResponse> {
  return api.get<SpendingByCategoryResponse>("/api/dashboard/spending-by-category");
}

export function getIncomeVsExpenses(): Promise<IncomeVsExpensesResponse> {
  return api.get<IncomeVsExpensesResponse>("/api/dashboard/income-vs-expenses");
}

export function getRecurringCharges(): Promise<RecurringChargesResponse> {
  return api.get<RecurringChargesResponse>("/api/dashboard/recurring-charges");
}
