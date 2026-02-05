import { api } from "./client";

export interface Label {
  id: number;
  name: string;
  color: string;
  created_at: string;
}

export interface LabelListResponse {
  items: Label[];
  total: number;
  page: number;
  page_size: number;
}

export interface ListLabelsParams {
  page?: number;
  page_size?: number;
  q?: string;
  sort_by?: string;
  sort_dir?: "asc" | "desc";
}

export function listLabels(params?: ListLabelsParams): Promise<LabelListResponse> {
  const search = new URLSearchParams();
  if (params?.page) search.set("page", String(params.page));
  if (params?.page_size) search.set("page_size", String(params.page_size));
  if (params?.q) search.set("q", params.q);
  if (params?.sort_by) search.set("sort_by", params.sort_by);
  if (params?.sort_dir) search.set("sort_dir", params.sort_dir);
  const qs = search.toString();
  return api.get<LabelListResponse>(`/api/labels${qs ? `?${qs}` : ""}`);
}

export function createLabel(data: { name: string; color?: string }): Promise<Label> {
  return api.post<Label>("/api/labels", data);
}

export function deleteLabel(id: number): Promise<void> {
  return api.delete<void>(`/api/labels/${id}`);
}
