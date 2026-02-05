import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import UploadPage from "../pages/UploadPage";

vi.mock("../api/transactions", () => ({
  importTransactions: vi.fn(),
  listTransactions: vi.fn(),
}));

describe("UploadPage", () => {
  it("renders the heading", () => {
    render(<UploadPage />);
    expect(screen.getByRole("heading", { name: /import transactions/i })).toBeInTheDocument();
  });

  it("renders the file input", () => {
    render(<UploadPage />);
    expect(screen.getByLabelText(/select csv file/i)).toBeInTheDocument();
  });

  it("has upload button disabled when no file selected", () => {
    render(<UploadPage />);
    expect(screen.getByRole("button", { name: /upload/i })).toBeDisabled();
  });

  it("displays CSV format instructions", () => {
    render(<UploadPage />);
    expect(screen.getByText(/csv format/i)).toBeInTheDocument();
  });
});
