import { api } from "./client";

export interface Todo {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
}

export interface TodoListResponse {
  items: Todo[];
  total: number;
  page: number;
  page_size: number;
}

export interface ListTodosParams {
  page?: number;
  page_size?: number;
  q?: string;
  sort_by?: string;
  sort_dir?: "asc" | "desc";
}

export function listTodos(params?: ListTodosParams): Promise<TodoListResponse> {
  const search = new URLSearchParams();
  if (params?.page) search.set("page", String(params.page));
  if (params?.page_size) search.set("page_size", String(params.page_size));
  if (params?.q) search.set("q", params.q);
  if (params?.sort_by) search.set("sort_by", params.sort_by);
  if (params?.sort_dir) search.set("sort_dir", params.sort_dir);
  const qs = search.toString();
  return api.get<TodoListResponse>(`/api/todos${qs ? `?${qs}` : ""}`);
}

export function createTodo(title: string): Promise<Todo> {
  return api.post<Todo>("/api/todos", { title });
}

export function deleteTodo(id: number): Promise<void> {
  return api.delete<void>(`/api/todos/${id}`);
}
