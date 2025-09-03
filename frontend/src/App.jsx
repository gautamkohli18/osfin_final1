import { useState } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "👋 Hi! Ask me anything about disputes or transactions." }
  ]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input.trim()) return;

    // Add user message
    setMessages([...messages, { sender: "user", text: input }]);

    // Send to backend
    const res = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input })
    });
    const data = await res.json();

    // Add bot reply
    setMessages(m => [...m, { sender: "bot", text: data.answer || "⚠️ Error: " + data.error }]);
    setInput("");
  }

  return (
    <div style={{ fontFamily: "sans-serif", background: "#f3f4f6", height: "100vh", padding: "20px" }}>
      <div style={{ maxWidth: "600px", margin: "0 auto", background: "#fff", borderRadius: "12px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)", display: "flex", flexDirection: "column",
                    height: "100%" }}>
        <div style={{ flex: 1, overflowY: "auto", padding: "10px" }}>
          {messages.map((msg, i) => (
            <div key={i} style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              margin: "5px 0"
            }}>
              <span style={{
                display: "inline-block",
                padding: "10px",
                borderRadius: "8px",
                background: msg.sender === "user" ? "#e0f2fe" : "#f1f5f9"
              }}>
                {msg.text}
              </span>
            </div>
          ))}
        </div>

        <div style={{ display: "flex", borderTop: "1px solid #ddd", padding: "10px" }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            placeholder="Type your question..."
            style={{ flex: 1, padding: "10px", borderRadius: "8px", border: "1px solid #ddd" }}
          />
          <button
            onClick={sendMessage}
            style={{ marginLeft: "8px", padding: "10px 16px", border: "none",
                     background: "#2563eb", color: "#fff", borderRadius: "8px", cursor: "pointer" }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
