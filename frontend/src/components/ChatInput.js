import React, { useState } from 'react';
import './ChatInput.css';

const ChatInput = ({ addMessage }) => {
    const [input, setInput] = useState('');

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSend = async () => {
        if (input.trim()) {
            // Add user message to chat
            const userMessage = { text: input, user: 'You' };
            addMessage(userMessage);

            try {
                // Send input to backend
                const response = await fetch('http://127.0.0.1:5000/claude/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: input }),
                });

                // Handle AI response
                if (response.ok) {
                    const data = await response.json();
                    const aiMessage = { text: data.response, user: 'AI' };
                    addMessage(aiMessage);
                } else {
                    addMessage({ text: 'Error: Failed to fetch AI response.', user: 'AI' });
                }
            } catch (error) {
                addMessage({ text: `Error: ${error.message}`, user: 'AI' });
            }

            setInput(''); // Clear input field
        }
    };

    return (
        <div className="chat-input">
            <input
                type="text"
                value={input}
                onChange={handleInputChange}
                placeholder="Type your question here..."
            />
            <button onClick={handleSend}>
                <i className="send-icon">➤</i>
            </button>
        </div>
    );
};

export default ChatInput;
