import React, { useState, useContext } from 'react';
import GlobalContext from '../context/GlobalContext';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const { setTicker, setScore } = useContext(GlobalContext);

    const addMessage = (message) => {
        setMessages((prevMessages) => [...prevMessages, message]);
    };

    const handleSendMessage = async (input) => {
        if (!input.trim()) return;

        addMessage({ text: input, user: 'You' });
        setLoading(true);

        try {
            const response = await fetch('http://localhost:5000/claude/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: input }),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.ticker) {
                    setTicker(data.ticker);
                }
                if (data.score) {
                    const score = typeof data.score === 'number' ? data.score : parseFloat(data.score);
                    setScore(score);
                }
                addMessage({ text: data.response, user: 'AI' });
            } else {
                addMessage({ text: 'Error: Failed to fetch AI response.', user: 'AI' });
            }
        } catch (error) {
            addMessage({ text: `Error: ${error.message}`, user: 'AI' });
        } finally {
            setLoading(false);
        }
    };

    const handleInputKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage(e.target.value);
            e.target.value = '';
        }
    };

    const handleButtonClick = () => {
        const inputField = document.getElementById('chat-input');
        if (inputField.value.trim()) {
            handleSendMessage(inputField.value);
            inputField.value = '';
        }
    };

    const formatMessage = (text) => {
        // Split the text by newlines and map each line to a paragraph or list item
        return text.split('\n').map((line, index) => {
            const trimmedLine = line.trim();
            if (!trimmedLine) return <br key={index} />;
            
            // Check if the line is a bullet point
            if (trimmedLine.startsWith('•')) {
                return (
                    <div key={index} className="bullet-point">
                        {trimmedLine}
                    </div>
                );
            }
            
            // Check if the line is a section header
            if (trimmedLine.endsWith(':')) {
                return (
                    <div key={index} className="section-header">
                        {trimmedLine}
                    </div>
                );
            }
            
            // Regular text
            return <div key={index} className="text-line">{trimmedLine}</div>;
        });
    };

    return (
        <div className="chatbot-widget">
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`chat-message ${message.user === 'AI' ? 'ai-message' : 'user-message'}`}
                    >
                        <div className="message-text">
                            {message.user === 'AI' ? formatMessage(message.text) : message.text}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="chat-message loading-bubble">
                        <div className="message-text">...</div>
                    </div>
                )}
            </div>
            <div className="chat-input">
                <input
                    id="chat-input"
                    type="text"
                    placeholder="Type your question here..."
                    onKeyDown={handleInputKeyDown}
                />
                <button onClick={handleButtonClick}>
                    <i className="send-icon">➤</i>
                </button>
            </div>
        </div>
    );
};

export default ChatbotWidget;