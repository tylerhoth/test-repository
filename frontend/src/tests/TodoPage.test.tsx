import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import TodoPage from "../pages/TodoPage";

const mockListTodos = vi.fn();
const mockCreateTodo = vi.fn();
const mockDeleteTodo = vi.fn();

vi.mock("../api/todos", () => ({
  listTodos: (...args: unknown[]) => mockListTodos(...args),
  createTodo: (...args: unknown[]) => mockCreateTodo(...args),
  deleteTodo: (...args: unknown[]) => mockDeleteTodo(...args),
}));

describe("TodoPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockListTodos.mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
    });
  });

  it("renders the heading", async () => {
    render(<TodoPage />);
    expect(screen.getByRole("heading", { name: /todos/i })).toBeInTheDocument();
    await waitFor(() => expect(mockListTodos).toHaveBeenCalled());
  });

  it("displays todos from the API", async () => {
    mockListTodos.mockResolvedValue({
      items: [
        { id: 1, title: "Buy milk", completed: false, created_at: "2024-01-01T00:00:00" },
        { id: 2, title: "Walk dog", completed: false, created_at: "2024-01-01T00:00:00" },
      ],
      total: 2,
      page: 1,
      page_size: 20,
    });

    render(<TodoPage />);

    await waitFor(() => {
      expect(screen.getByText("Buy milk")).toBeInTheDocument();
      expect(screen.getByText("Walk dog")).toBeInTheDocument();
    });
    expect(screen.getByText("2 todo(s)")).toBeInTheDocument();
  });

  it("creates a new todo", async () => {
    const user = userEvent.setup();
    mockCreateTodo.mockResolvedValue({ id: 1, title: "New task", completed: false });

    render(<TodoPage />);

    await waitFor(() => expect(mockListTodos).toHaveBeenCalled());

    const input = screen.getByLabelText("New todo title");
    await user.type(input, "New task");
    await user.click(screen.getByRole("button", { name: /add/i }));

    expect(mockCreateTodo).toHaveBeenCalledWith("New task");
  });

  it("deletes a todo", async () => {
    const user = userEvent.setup();
    mockListTodos.mockResolvedValue({
      items: [{ id: 1, title: "Delete me", completed: false, created_at: "2024-01-01T00:00:00" }],
      total: 1,
      page: 1,
      page_size: 20,
    });
    mockDeleteTodo.mockResolvedValue(undefined);

    render(<TodoPage />);

    await waitFor(() => expect(screen.getByText("Delete me")).toBeInTheDocument());

    await user.click(screen.getByRole("button", { name: /delete delete me/i }));

    expect(mockDeleteTodo).toHaveBeenCalledWith(1);
  });

  it("shows error on fetch failure", async () => {
    mockListTodos.mockRejectedValue(new Error("Network error"));

    render(<TodoPage />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Network error");
    });
  });
});
