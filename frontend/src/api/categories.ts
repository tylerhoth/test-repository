import { api } from "./client";

export interface Category {
  id: number;
  name: string;
  is_system: boolean;
  created_at: string;
}

export interface CategoryListResponse {
  items: Category[];
  total: number;
  page: number;
  page_size: number;
}

export interface ListCategoriesParams {
  page?: number;
  page_size?: number;
  q?: string;
  sort_by?: string;
  sort_dir?: "asc" | "desc";
}

export function listCategories(params?: ListCategoriesParams): Promise<CategoryListResponse> {
  const search = new URLSearchParams();
  if (params?.page) search.set("page", String(params.page));
  if (params?.page_size) search.set("page_size", String(params.page_size));
  if (params?.q) search.set("q", params.q);
  if (params?.sort_by) search.set("sort_by", params.sort_by);
  if (params?.sort_dir) search.set("sort_dir", params.sort_dir);
  const qs = search.toString();
  return api.get<CategoryListResponse>(`/api/categories${qs ? `?${qs}` : ""}`);
}

export function createCategory(data: { name: string }): Promise<Category> {
  return api.post<Category>("/api/categories", data);
}
