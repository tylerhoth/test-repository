import { useCallback, useEffect, useState } from "react";
import type { Label, LabelListResponse } from "../api/labels";
import { createLabel, deleteLabel, listLabels } from "../api/labels";

export default function LabelsPage() {
  const [data, setData] = useState<LabelListResponse | null>(null);
  const [newName, setNewName] = useState("");
  const [newColor, setNewColor] = useState("#6B7280");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLabels = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listLabels();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to fetch labels");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLabels();
  }, [fetchLabels]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    try {
      await createLabel({ name: newName.trim(), color: newColor });
      setNewName("");
      setNewColor("#6B7280");
      await fetchLabels();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create label");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteLabel(id);
      await fetchLabels();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete label");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Labels</h1>

      <form onSubmit={handleCreate} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Label name..."
          aria-label="New label name"
          style={{ flex: 1, padding: 8 }}
        />
        <input
          type="color"
          value={newColor}
          onChange={(e) => setNewColor(e.target.value)}
          aria-label="Label color"
          style={{ width: 40, height: 36, padding: 0, border: "1px solid #ddd" }}
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
          <p>{data.total} label(s)</p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {data.items.map((label: Label) => (
              <li
                key={label.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "8px 0",
                  borderBottom: "1px solid #eee",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span
                    style={{
                      display: "inline-block",
                      width: 16,
                      height: 16,
                      borderRadius: "50%",
                      backgroundColor: label.color,
                    }}
                  />
                  <span>{label.name}</span>
                </div>
                <button onClick={() => handleDelete(label.id)} aria-label={`Delete ${label.name}`}>
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
