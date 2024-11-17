import React from 'react';
import ChatbotWidget from './components/ChatbotWidget';
import './App.css';

const App = () => {
    return (
        <div className="app-container">
            <div className="left-column">
                {/* Left column content will be added later */}
            </div>
            <div className="right-column">
                <ChatbotWidget />
            </div>
        </div>
    );
};

export default App;