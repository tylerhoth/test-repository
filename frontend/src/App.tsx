import { useState } from "react";
import DashboardPage from "./pages/DashboardPage";
import TransactionsPage from "./pages/TransactionsPage";
import BudgetsPage from "./pages/BudgetsPage";
import AccountsPage from "./pages/AccountsPage";
import UploadPage from "./pages/UploadPage";
import LabelsPage from "./pages/LabelsPage";
import TodoPage from "./pages/TodoPage";

type Page = "dashboard" | "transactions" | "budgets" | "accounts" | "upload" | "labels" | "todos";

function App() {
  const [currentPage, setCurrentPage] = useState<Page>("dashboard");

  const navButtonStyle = (page: Page): React.CSSProperties => ({
    padding: "12px 24px",
    border: "none",
    backgroundColor: currentPage === page ? "#007bff" : "#f5f5f5",
    color: currentPage === page ? "white" : "#333",
    cursor: "pointer",
    fontSize: 16,
    fontWeight: currentPage === page ? "bold" : "normal",
  });

  return (
    <div>
      {/* Navigation Bar */}
      <nav
        style={{
          backgroundColor: "#fff",
          borderBottom: "2px solid #ddd",
          padding: "0",
          marginBottom: 0,
        }}
      >
        <div
          style={{
            maxWidth: 1200,
            margin: "0 auto",
            display: "flex",
            gap: 0,
          }}
        >
          <button style={navButtonStyle("dashboard")} onClick={() => setCurrentPage("dashboard")}>
            Dashboard
          </button>
          <button
            style={navButtonStyle("transactions")}
            onClick={() => setCurrentPage("transactions")}
          >
            Transactions
          </button>
          <button style={navButtonStyle("budgets")} onClick={() => setCurrentPage("budgets")}>
            Budgets
          </button>
          <button style={navButtonStyle("accounts")} onClick={() => setCurrentPage("accounts")}>
            Accounts
          </button>
          <button style={navButtonStyle("upload")} onClick={() => setCurrentPage("upload")}>
            Upload
          </button>
          <button style={navButtonStyle("labels")} onClick={() => setCurrentPage("labels")}>
            Labels
          </button>
          <button style={navButtonStyle("todos")} onClick={() => setCurrentPage("todos")}>
            Todos
          </button>
        </div>
      </nav>

      {/* Page Content */}
      {currentPage === "dashboard" && <DashboardPage />}
      {currentPage === "transactions" && <TransactionsPage />}
      {currentPage === "budgets" && <BudgetsPage />}
      {currentPage === "accounts" && <AccountsPage />}
      {currentPage === "upload" && <UploadPage />}
      {currentPage === "labels" && <LabelsPage />}
      {currentPage === "todos" && <TodoPage />}
    </div>
  );
}

export default App;
