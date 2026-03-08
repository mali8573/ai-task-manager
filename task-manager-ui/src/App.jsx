import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // גלילה אוטומטית לסוף הצ'אט
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_id: "default_user", // מזהה קבוע לדוגמה
          message: input 
        }),
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'agent', content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'agent', content: "שגיאה בחיבור לשרת" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-wrapper">
    <div className="chat-app" dir="rtl">
      <header>
        <h1>ניהול משימות חכם 🤖</h1>
      </header>
      
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message-bubble ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && <div className="message-bubble agent typing">...מקליד</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="איך אפשר לעזור?"
        />
        <button onClick={sendMessage} disabled={loading}>שלח</button>
      </div>
    </div>
    </div>
  );
}

export default App;