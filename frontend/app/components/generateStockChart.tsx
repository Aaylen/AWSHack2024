"use client";
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Registering the necessary components for Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface StockChartProps {
    ticker: string;
}

const GenerateStockChart: React.FC<StockChartProps> = ({ ticker }) => {
    const [stockData, setStockData] = useState<any>(null);  // Stock data to pass to chart
    const [timeframe, setTimeframe] = useState<string>('5d'); // Default timeframe
    const [keyMetrics, setKeyMetrics] = useState<any>(null); // To store P/E and Market Cap

    // Function to fetch stock data from API
    const fetchStockData = async () => {
        try {
            const result = await axios.post('http://localhost:5000/stocks/endpoint', { ticker, entry: timeframe });
            setStockData(result.data);
            setKeyMetrics(result.data.key_metrics);  // Assuming the backend sends key metrics like P/E, Market Cap
        } catch (error) {
            console.error('Error fetching stock data', error);
        }
    };

    useEffect(() => {
        fetchStockData();
    }, [timeframe]); // Fetch new data when timeframe changes

    // Chart data setup
    const chartData = {
        labels: stockData ? stockData.dates : [],
        datasets: [
            {
                label: 'Closing Prices',
                data: stockData ? stockData.closing_prices : [],
                borderColor: 'rgb(75, 192, 192)',
                fill: false,
            },
            {
                label: 'Opening Prices',
                data: stockData ? stockData.opening_prices : [],
                borderColor: 'rgb(255, 99, 132)',
                fill: false,
            },
        ],
    };

    // Button to toggle between 5d, YTD, etc.
    const handleTimeframeChange = (newTimeframe: string) => {
        setTimeframe(newTimeframe);
    };

    return (
        <div>
            <button onClick={() => handleTimeframeChange('5d')}>5 Day</button>
            <button onClick={() => handleTimeframeChange('ytd')}>YTD</button>
            {keyMetrics && (
                <div>
                    <p>P/E Ratio: {keyMetrics.pe}</p>
                    <p>Market Cap: {keyMetrics.marketCap}</p>
                </div>
            )}
            <div>
                {stockData ? (
                    <Line data={chartData} />
                ) : (
                    <p>Loading chart...</p>
                )}
            </div>
        </div>
    );
};

export default GenerateStockChart;
