import { api } from "./client";

export interface Transaction {
  id: number;
  date: string;
  description: string;
  raw_description: string | null;
  amount: number;
  category_id: number | null;
  account_id: number | null;
  is_recurring: boolean;
  tags: string | null;
  notes: string | null;
  created_at: string;
}

export interface TransactionListResponse {
  items: Transaction[];
  total: number;
  page: number;
  page_size: number;
}

export interface ImportResult {
  imported: number;
  skipped: number;
  accounts_created: number;
  categories_created: number;
}

export interface ListTransactionsParams {
  page?: number;
  page_size?: number;
  q?: string;
  sort_by?: string;
  sort_dir?: "asc" | "desc";
  account_id?: number;
  category_id?: number;
  date_from?: string;
  date_to?: string;
}

export interface CreateTransactionData {
  date: string;
  description: string;
  amount: number;
  category_id?: number | null;
  account_id?: number | null;
  is_recurring?: boolean;
  tags?: string | null;
  notes?: string | null;
}

export interface UpdateTransactionData {
  date?: string;
  description?: string;
  amount?: number;
  category_id?: number | null;
  account_id?: number | null;
  is_recurring?: boolean;
  tags?: string | null;
  notes?: string | null;
}

export function listTransactions(
  params?: ListTransactionsParams,
): Promise<TransactionListResponse> {
  const search = new URLSearchParams();
  if (params?.page) search.set("page", String(params.page));
  if (params?.page_size) search.set("page_size", String(params.page_size));
  if (params?.q) search.set("q", params.q);
  if (params?.sort_by) search.set("sort_by", params.sort_by);
  if (params?.sort_dir) search.set("sort_dir", params.sort_dir);
  if (params?.account_id) search.set("account_id", String(params.account_id));
  if (params?.category_id) search.set("category_id", String(params.category_id));
  if (params?.date_from) search.set("date_from", params.date_from);
  if (params?.date_to) search.set("date_to", params.date_to);
  const qs = search.toString();
  return api.get<TransactionListResponse>(`/api/transactions${qs ? `?${qs}` : ""}`);
}

export function createTransaction(data: CreateTransactionData): Promise<Transaction> {
  return api.post<Transaction>("/api/transactions", data);
}

export function updateTransaction(id: number, data: UpdateTransactionData): Promise<Transaction> {
  return api.put<Transaction>(`/api/transactions/${id}`, data);
}

export function deleteTransaction(id: number): Promise<void> {
  return api.delete<void>(`/api/transactions/${id}`);
}

export function importTransactions(file: File): Promise<ImportResult> {
  const formData = new FormData();
  formData.append("file", file);
  return api.postFile<ImportResult>("/api/transactions/import", formData);
}
