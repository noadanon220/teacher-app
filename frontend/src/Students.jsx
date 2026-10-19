import { useEffect, useState } from "react";
import { request } from "./api";

const emptyForm = { name: "", class_name: "", phone: "" };

export default function Students({ onLogout }) {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null); // null = adding a new student
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function loadStudents() {
    try {
      setStudents(await request("/students"));
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadStudents();
  }, []);

  function validate() {
    if (!form.name.trim()) return "Enter a name";
    if (!form.class_name.trim()) return "Enter a class";
    if (!/^05\d{8}$/.test(form.phone))
      return "Phone must be a 10-digit mobile number (05XXXXXXXX)";
    return "";
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage("");
    const problem = validate();
    if (problem) {
      setError(problem);
      return;
    }
    setError("");

    try {
      if (editingId) {
        await request(`/students/${editingId}`, {
          method: "PUT",
          body: JSON.stringify(form),
        });
        setMessage("Student updated");
      } else {
        await request("/students", {
          method: "POST",
          body: JSON.stringify(form),
        });
        setMessage("Student added");
      }
      setForm(emptyForm);
      setEditingId(null);
      loadStudents();
    } catch (err) {
      setError(err.message);
    }
  }

  function startEdit(student) {
    setEditingId(student.id);
    setForm({
      name: student.name,
      class_name: student.class_name,
      phone: student.phone,
    });
    setError("");
    setMessage("");
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
    setError("");
  }

  return (
    <div className="page">
      <header>
        <h1>My students</h1>
        <button className="secondary" onClick={onLogout}>
          Log out
        </button>
      </header>

      <form className="card" onSubmit={handleSubmit}>
        <h2>{editingId ? "Edit student" : "Add student"}</h2>
        <div className="row">
          <div>
            <label>Name</label>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </div>
          <div>
            <label>Class</label>
            <input
              value={form.class_name}
              onChange={(e) => setForm({ ...form, class_name: e.target.value })}
            />
          </div>
          <div>
            <label>Phone</label>
            <input
              value={form.phone}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
              inputMode="numeric"
              maxLength={10}
            />
          </div>
        </div>

        {error && <p className="error">{error}</p>}
        {message && <p className="success">{message}</p>}

        <div className="actions">
          <button type="submit">
            {editingId ? "Save changes" : "Add student"}
          </button>
          {editingId && (
            <button type="button" className="secondary" onClick={cancelEdit}>
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="card">
        {students.length === 0 ? (
          <p className="muted">No students yet. Add the first one above.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Class</th>
                <th>Phone</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.class_name}</td>
                  <td>{s.phone}</td>
                  <td>
                    <button
                      className="secondary small"
                      onClick={() => startEdit(s)}
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
