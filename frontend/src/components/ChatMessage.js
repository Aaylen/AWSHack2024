import React from 'react';


const ChatMessage = ({ message }) => {
    return (
        <div className={`chat-message ${message.user === 'AI' ? 'ai-message' : 'user-message'}`}>
            <div className="message-text">{message.text}</div>
        </div>
    );
};

export default ChatMessage;
