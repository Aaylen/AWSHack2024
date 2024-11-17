import React from 'react';
import Chart from './components/Chart';
import ChatbotWidget from './components/ChatbotWidget';
import './components/styles.css';

const App = () => {
    return (
        <div className="app-container">
            <div className="chart-section">
                <Chart />
            </div>
            <div className="chatbot-section">
                <ChatbotWidget />
            </div>
        </div>
    );
};

export default App;
