import React, { useState } from 'react';
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export default function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  async function send(event) {
    event.preventDefault();
    const message = input.trim();
    if (!message || loading) return;
    setInput(''); setError(''); setLoading(true);
    setMessages(old => [...old, { role: 'user', text: message }]);
    try {
      const response = await fetch(`${API}/chat`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message }) });
      if (!response.ok) throw new Error(response.status === 503 ? 'Answer service is temporarily unavailable.' : 'Unable to send message.');
      const data = await response.json();
      setMessages(old => [...old, { role: 'assistant', text: data.answer, sources: data.sources }]);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  }
  return <main className="shell"><header><span className="mark">✦</span><div><h1>College FAQ Assistant</h1><p>Ask about admissions, fees, scholarships, hostel or placements.</p></div></header>
    <section className="chat" aria-live="polite">{messages.length === 0 && <div className="welcome"><h2>How can I help?</h2><p>Try: “How do I apply for admission?”</p></div>}
      {messages.map((m, i) => <article className={`bubble ${m.role}`} key={i}><div>{m.text}</div>{m.sources?.length > 0 && <aside><strong>Sources</strong>{m.sources.map(s => <span key={s.id}>{s.id} · {s.question}</span>)}</aside>}</article>)}
      {loading && <p className="status" role="status">Finding an answer…</p>}
    </section>
    {error && <p className="error" role="alert">{error} Please try again.</p>}
    <form onSubmit={send}><input aria-label="Your question" maxLength={1000} value={input} onChange={e => setInput(e.target.value)} placeholder="Ask a college question…"/><button disabled={loading || !input.trim()} type="submit">Send</button></form>
    <footer>Answers are based on sample FAQs. Verify important details with the college.</footer></main>;
}
