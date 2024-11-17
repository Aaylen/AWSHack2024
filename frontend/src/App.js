import React, { useContext } from 'react';
import ChatbotWidget from './components/ChatbotWidget';
import StockChart from './components/generateStockChart.js';
import GlobalContext from './context/GlobalContext';
import './App.css';

const App = () => {
    const { ticker } = useContext(GlobalContext);
    
    return (
        <div className="app-container">
            <div className="left-column">
                <StockChart ticker={ticker} />
            </div>
            <div className="right-column">
                <ChatbotWidget />
            </div>
        </div>
    );
};

export default App;
