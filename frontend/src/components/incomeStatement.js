import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './incomeStatement.css';

const IncomeStatement = ({ ticker }) => {
    const [incomeData, setIncomeData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                console.log('Fetching income data for', ticker);
                const response = await axios.post('http://localhost:5000/income/endpoint', { ticker: ticker });
                setIncomeData(response.data.most_recent_quarter);
                console.log('Income data:', response.data.most_recent_quarter);
            } catch (err) {
                setError(err.message || 'Failed to fetch data');
            } finally {
                setLoading(false);
            }
        };

        if (ticker) {
            fetchData();
        }
    }, [ticker]);

    const formatNumber = (num) => {
        if (num === null || num === undefined || isNaN(num)) return '-';
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
            notation: "compact",
            compactDisplay: "short"
        }).format(num);
    };

    // Custom order for income statement items
    const itemOrder = [
        'Total Revenue',
        'Cost Of Revenue',
        'Gross Profit',
        'Operating Expense',
        'Research And Development',
        'Selling General And Administration',
        'Operating Income',
        'Other Non Operating Income Expenses',
        'Pretax Income',
        'Tax Provision',
        'Net Income',
        'EBIT',
        'EBITDA',
        'Normalized EBITDA'
    ];

    if (loading) {
        return <div className="income-loading">Loading...</div>;
    }

    if (error) {
        return <div className="income-error">Error: {error}</div>;
    }

    if (!incomeData || !incomeData.data) {
        return <div className="income-empty">No data available</div>;
    }

    return (
        <div className="income-container">
            <h2 className="income-title">
                {ticker} Income Statement
            </h2>
            <h3 className="income-subtitle">
                Quarter Ending {new Date(incomeData.date).toLocaleDateString()}
            </h3>
            <div className="table-container">
                <table className="income-table">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {itemOrder.map((key) => {
                            const value = incomeData.data[key];
                            if (value === undefined) return null;
                            return (
                                <tr key={key} className={key === 'Net Income' ? 'highlight-row' : ''}>
                                    <td className="label">{key}</td>
                                    <td className={`value ${value < 0 ? 'negative' : ''}`}>
                                        {formatNumber(value)}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default IncomeStatement;