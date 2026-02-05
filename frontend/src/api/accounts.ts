import { api } from "./client";

export interface Account {
  id: number;
  name: string;
  institution: string;
  account_type: string;
  last_four: string | null;
  created_at: string;
}

export interface AccountListResponse {
  items: Account[];
  total: number;
  page: number;
  page_size: number;
}

export interface ListAccountsParams {
  page?: number;
  page_size?: number;
  q?: string;
  sort_by?: string;
  sort_dir?: "asc" | "desc";
}

export function listAccounts(params?: ListAccountsParams): Promise<AccountListResponse> {
  const search = new URLSearchParams();
  if (params?.page) search.set("page", String(params.page));
  if (params?.page_size) search.set("page_size", String(params.page_size));
  if (params?.q) search.set("q", params.q);
  if (params?.sort_by) search.set("sort_by", params.sort_by);
  if (params?.sort_dir) search.set("sort_dir", params.sort_dir);
  const qs = search.toString();
  return api.get<AccountListResponse>(`/api/accounts${qs ? `?${qs}` : ""}`);
}
