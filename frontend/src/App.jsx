import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadTickets = async () => {
    const response = await fetch(`${API_URL}/tickets`);
    const data = await response.json();
    setTickets(data);
  };

  useEffect(() => {
    loadTickets();
  }, []);

  const createTicket = async (event) => {
    event.preventDefault();

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/tickets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          description,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create ticket");
      }

      setTitle("");
      setDescription("");

      await loadTickets();
    } catch (error) {
      console.error(error);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Support Ticket Assistant</h1>

      <p className="subtitle">
        AI-powered ticket classification and prioritization
      </p>

      <form onSubmit={createTicket} className="ticket-form">
        <h2>Create Support Ticket</h2>

        <label>Title</label>

        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Example: Production API unavailable"
          required
        />

        <label>Description</label>

        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Describe the problem..."
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "AI is analyzing..." : "Analyze & Create Ticket"}
        </button>
      </form>

      <h2>Support Tickets</h2>

      <div className="tickets">
        {tickets.map((ticket) => (
          <div className="ticket" key={ticket.id}>
            <div className="ticket-header">
              <h3>{ticket.title}</h3>

              <span className={`priority ${ticket.priority?.toLowerCase()}`}>
                {ticket.priority}
              </span>
            </div>

            <p>{ticket.description}</p>

            <div className="ai-result">
              <p>
                <strong>Category:</strong> {ticket.category}
              </p>

              <p>
                <strong>AI Summary:</strong> {ticket.summary}
              </p>

              <p>
                <strong>Suggested Action:</strong>{" "}
                {ticket.suggested_action}
              </p>

              <p>
                <strong>Status:</strong> {ticket.status}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;