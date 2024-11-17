import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (message) => {
        setMessages([...messages, { text: message, user: 'You' }, { text: 'Response from AI', user: 'AI' }]);
    };

    return (
        <div className="chatbot-widget">
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <ChatMessage key={index} message={message} />
                ))}
            </div>
            <ChatInput onSendMessage={handleSendMessage} />
        </div>
    );
};

export default ChatbotWidget;