import React, { useContext } from 'react';
import ChatbotWidget from './components/ChatbotWidget';
import StockChart from './components/generateStockChart.js';
import GlobalContext from './context/GlobalContext';
import IncomeStatement from './components/incomeStatement.js';
import BalanceSheetWidget from './components/BalanceSheetWidget';
import CashflowStatement from './components/cashflowStatement.js';
import './App.css';
import logo from './components/logo.png';

const App = () => {
    const { ticker } = useContext(GlobalContext);
    const { score } = useContext(GlobalContext);

    return (
        <div className="app-container">
            <div className="content">
                <div className="left-column max-h-screen sticky top-0 overflow-y-auto">
                    <StockChart ticker={ticker} />
                    <BalanceSheetWidget ticker={ticker} />
                    <IncomeStatement ticker={ticker} />
                    <CashflowStatement ticker={ticker} />
                </div>
                <div className="right-column">
                    <ChatbotWidget />
                </div>
            </div>
        </div>
    );
};

export default App;