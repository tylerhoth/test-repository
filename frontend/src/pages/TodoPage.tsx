import { useCallback, useEffect, useState } from "react";
import type { Todo, TodoListResponse } from "../api/todos";
import { createTodo, deleteTodo, listTodos } from "../api/todos";

export default function TodoPage() {
  const [data, setData] = useState<TodoListResponse | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTodos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listTodos();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch todos");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      await createTodo(newTitle.trim());
      setNewTitle("");
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create todo");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTodo(id);
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete todo");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Todos</h1>

      <form onSubmit={handleCreate} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="New todo..."
          aria-label="New todo title"
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit">Add</button>
      </form>

      {error && (
        <p role="alert" style={{ color: "red" }}>
          {error}
        </p>
      )}
      {loading && <p>Loading...</p>}

      {data && (
        <>
          <p>{data.total} todo(s)</p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {data.items.map((todo: Todo) => (
              <li
                key={todo.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "8px 0",
                  borderBottom: "1px solid #eee",
                }}
              >
                <span>{todo.title}</span>
                <button onClick={() => handleDelete(todo.id)} aria-label={`Delete ${todo.title}`}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
