import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './cashflowStatement.css';

const CashflowStatement = ({ ticker }) => {
    const [cashflowData, setCashflowData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                console.log('Fetching cashflow data for', ticker);
                const response = await axios.post('http://localhost:5000/cashflow/endpoint', { ticker: ticker });
                setCashflowData(response.data.most_recent_quarter);
                console.log('Cashflow data:', response.data.most_recent_quarter);
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

    // Custom order for cash flow statement items
    const itemOrder = [
        'Net Income',
        'Depreciation',
        'Changes In Accounts Receivables',
        'Changes In Liabilities',
        'Changes In Inventories',
        'Cash From Operating Activities',
        'Capital Expenditures',
        'Investments',
        'Cash From Investing Activities',
        'Dividends Paid',
        'Issuance Of Stock',
        'Issuance Of Debt',
        'Cash From Financing Activities',
        'Change In Cash'
    ];

    if (loading) {
        return;
    }

    if (error) {
        return;
    }

    if (!cashflowData || !cashflowData.data) {
        return;
    }

    return (
        <div className="cashflow-container">
            <h2 className="cashflow-title">
                {ticker} Cash Flow Statement
            </h2>
            <h3 className="cashflow-subtitle">
                Quarter Ending {new Date(cashflowData.date).toLocaleDateString()}
            </h3>
            <div className="table-container">
                <table className="cashflow-table">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {itemOrder.map((key) => {
                            const value = cashflowData.data[key];
                            if (value === undefined) return null;
                            return (
                                <tr key={key} className={key === 'Change In Cash' ? 'highlight-row' : ''}>
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

export default CashflowStatement;
