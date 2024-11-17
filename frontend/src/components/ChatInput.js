import React, { useState } from 'react';
import './ChatInput.css';

const ChatInput = ({ onSendMessage }) => {
    const [input, setInput] = useState('');

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSend = () => {
        if (input.trim()) {
            onSendMessage(input);
            setInput('');
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