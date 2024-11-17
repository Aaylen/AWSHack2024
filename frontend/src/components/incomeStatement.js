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
                const response = await axios.post('http://localhost:5000/income/endpoint', { ticker: ticker });
                setIncomeData(response.data.most_recent_quarter);
                console.log("Response", response.data.most_recent_quarter);
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
        if (num === null || num === undefined) return '-';
        // Convert to millions and format with 2 decimal places
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
        'totalRevenue',
        'costOfRevenue',
        'grossProfit',
        'operatingExpenses',
        'sellingGeneralAdministrative',
        'researchDevelopment',
        'operatingIncome',
        'interestExpense',
        'totalOtherIncomeExpenseNet',
        'incomeBeforeTax',
        'incomeTaxExpense',
        'netIncome',
        'netIncomeApplicableToCommonShares',
        'ebit',
        'ebitda'
    ];

    if (loading) {
        return <div className="income-loading">Loading...</div>;
    }

    if (error) {
        return <div className="income-error">Error: {error}</div>;
    }

    if (!incomeData) {
        return <div className="income-empty">No data available</div>;
    }

    const formatLabel = (label) => {
        // Convert camelCase to Title Case with spaces
        return label
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .trim()
            .replace('E B I T D A', 'EBITDA')
            .replace('E B I T', 'EBIT');
    };

    const sortedItems = itemOrder.filter(item => incomeData.data[item] !== undefined);

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
                        {sortedItems.map((key) => (
                            <tr key={key} className={key === 'netIncome' ? 'highlight-row' : ''}>
                                <td className="label">{formatLabel(key)}</td>
                                <td className={`value ${incomeData.data[key] < 0 ? 'negative' : ''}`}>
                                    {formatNumber(incomeData.data[key])}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default IncomeStatement;