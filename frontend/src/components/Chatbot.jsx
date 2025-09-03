import { useState } from "react";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [table, setTable] = useState("disputes");

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "You", text: input };
    setMessages((prev) => [...prev, userMessage]);
    try {
      const res = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input, table }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { sender: "Bot", text: data.answer }]);
    } catch {
      setMessages((prev) => [...prev, { sender: "Bot", text: "⚠️ Error" }]);
    }
    setInput("");
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-4 flex flex-col h-[70vh]">
      <div className="flex-1 overflow-y-auto space-y-2 mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded-2xl max-w-xs ${
              msg.sender === "You"
                ? "bg-indigo-500 text-white self-end ml-auto"
                : "bg-gray-100 text-gray-800"
            } shadow-md`}
          >
            <span className="block text-sm opacity-70">{msg.sender}</span>
            <span className="block">{msg.text}</span>
          </div>
        ))}
      </div>
      <div className="flex items-center space-x-2 mb-2">
        <select
          value={table}
          onChange={(e) => setTable(e.target.value)}
          className="p-2 rounded-xl border border-gray-300 shadow-sm"
        >
          <option value="disputes">📊 Disputes</option>
          <option value="resolutions">📝 Resolutions</option>
          <option value="case_history">📂 Case History</option>
          <option value="multi">🔀 Multi-table (join)</option>
        </select>
      </div>
      <div className="flex items-center space-x-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e)=> e.key==="Enter" && sendMessage()}
          placeholder="Ask a question..."
          className="flex-1 p-3 rounded-xl border border-gray-300 shadow-sm"
        />
        <button
          onClick={sendMessage}
          className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-4 py-2 rounded-xl shadow-md"
        >
          Send
        </button>
      </div>
    </div>
  );
}
