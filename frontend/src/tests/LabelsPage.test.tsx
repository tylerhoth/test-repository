import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import LabelsPage from "../pages/LabelsPage";

const mockListLabels = vi.fn();
const mockCreateLabel = vi.fn();
const mockDeleteLabel = vi.fn();

vi.mock("../api/labels", () => ({
  listLabels: (...args: unknown[]) => mockListLabels(...args),
  createLabel: (...args: unknown[]) => mockCreateLabel(...args),
  deleteLabel: (...args: unknown[]) => mockDeleteLabel(...args),
}));

describe("LabelsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockListLabels.mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      page_size: 20,
    });
  });

  it("renders the heading", async () => {
    render(<LabelsPage />);
    expect(screen.getByRole("heading", { name: /labels/i })).toBeInTheDocument();
    await waitFor(() => expect(mockListLabels).toHaveBeenCalled());
  });

  it("displays labels from the API", async () => {
    mockListLabels.mockResolvedValue({
      items: [
        { id: 1, name: "Work", color: "#3B82F6", created_at: "2026-01-01T00:00:00" },
        { id: 2, name: "Personal", color: "#10B981", created_at: "2026-01-01T00:00:00" },
      ],
      total: 2,
      page: 1,
      page_size: 20,
    });

    render(<LabelsPage />);
    await waitFor(() => {
      expect(screen.getByText("Work")).toBeInTheDocument();
      expect(screen.getByText("Personal")).toBeInTheDocument();
    });
    expect(screen.getByText("2 label(s)")).toBeInTheDocument();
  });

  it("creates a new label", async () => {
    const user = userEvent.setup();
    mockCreateLabel.mockResolvedValue({ id: 1, name: "New Label", color: "#6B7280" });

    render(<LabelsPage />);
    await waitFor(() => expect(mockListLabels).toHaveBeenCalled());

    const input = screen.getByLabelText("New label name");
    await user.type(input, "New Label");
    await user.click(screen.getByRole("button", { name: /add/i }));

    expect(mockCreateLabel).toHaveBeenCalledWith({ name: "New Label", color: "#6B7280" });
  });

  it("deletes a label", async () => {
    const user = userEvent.setup();
    mockListLabels.mockResolvedValue({
      items: [{ id: 1, name: "Delete me", color: "#EF4444", created_at: "2026-01-01T00:00:00" }],
      total: 1,
      page: 1,
      page_size: 20,
    });
    mockDeleteLabel.mockResolvedValue(undefined);

    render(<LabelsPage />);
    await waitFor(() => expect(screen.getByText("Delete me")).toBeInTheDocument());
    await user.click(screen.getByRole("button", { name: /delete delete me/i }));

    expect(mockDeleteLabel).toHaveBeenCalledWith(1);
  });

  it("shows error on fetch failure", async () => {
    mockListLabels.mockRejectedValue(new Error("Network error"));
    render(<LabelsPage />);
    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Network error");
    });
  });
});
