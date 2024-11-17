import React, { useState } from 'react';

const ChatbotWidget = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSendMessage = () => {
        if (input.trim()) {
            setMessages([...messages, { text: input, sender: 'user' }]);
            setInput('');
            setTimeout(() => {
                setMessages((prev) => [...prev, { text: 'AI Response', sender: 'bot' }]);
            }, 500);
        }
    };

    return (
        <div className="chatbot-widget">
            <div className="chatbot-header">AI Chatbot</div>
            <div className="chatbot-messages">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.sender === 'user' ? 'user' : 'bot'}`}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <div className="chatbot-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default ChatbotWidget;
