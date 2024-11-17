import React from 'react';
import ChatbotWidget from './components/ChatbotWidget';
import StockChart from './components/generateStockChart.js';
import './App.css';

const App = () => {
    return (
        <div className="app-container">
            <div className="left-column">
                {/* Left column content will be added later */}
                <StockChart ticker= 'AAPL' />
            </div>
            <div className="right-column">
                <ChatbotWidget />
            </div>
        </div>
    );
};

export default App;