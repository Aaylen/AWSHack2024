import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './BalanceSheetWidget.css';

const BalanceSheetWidget = ({ ticker }) => {
    const [balanceSheet, setBalanceSheet] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (ticker) {
            fetch(`http://localhost:5000/stocks/balance-sheet/${ticker}`)
                .then((response) => {
                    if (!response.ok) throw new Error("Failed to fetch balance sheet data.");
                    return response.json();
                })
                .then((data) => {
                    setBalanceSheet(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err.message);
                    setLoading(false);
                });
        }
    }, [ticker]);

    if (loading) return <div>Loading balance sheet...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="balance-sheet-widget">
            <h2>Balance Sheet for {ticker}</h2>
            {balanceSheet ? (
                <table>
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(balanceSheet).map(([key, value]) => (
                            <tr key={key}>
                                <td>{key}</td>
                                <td>{value}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No balance sheet data available.</p>
            )}
        </div>
    );
};

BalanceSheetWidget.propTypes = {
    ticker: PropTypes.string.isRequired,
};

export default BalanceSheetWidget;
