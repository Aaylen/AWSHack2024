import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const GenerateStockChart = ({ ticker }) => {
    const [stockData, setStockData] = useState(null);
    const [timeframe, setTimeframe] = useState('5d');
    const [currentPrice, setCurrentPrice] = useState(null);
    const [priceChange, setPriceChange] = useState(null);
    const [percentChange, setPercentChange] = useState(null);

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        
        switch (timeframe) {
            case '1d':
                return date.toLocaleTimeString('en-US', { hour: 'numeric', hour12: true });
            case '5d':
            case '1mo':
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            case '6mo':
            case '1y':
                return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
            case '5y':
            case 'max':
                return date.toLocaleDateString('en-US', { year: 'numeric' });
            default:
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }
    };

    const getTickCount = () => {
        switch (timeframe) {
            case '1d': return 4;
            case '5d': return 5;
            case '1mo': return 4;
            case '6mo': return 6;
            case '1y': return 4;
            case '5y': return 5;
            case 'max': return 5;
            default: return 5;
        }
    };

    const fetchStockData = async () => {
        try {
            const response = await axios.post('http://localhost:5000/stocks/endpoint', {
                action: 'display_stock',
                ticker: ticker,
                entry: timeframe
            });
            
            if (response.data.chart) {
                setStockData(response.data.chart);
                
                const prices = response.data.chart.closing_prices;
                const currentPrice = prices[prices.length - 1];
                const previousPrice = prices[0];
                const priceChange = currentPrice - previousPrice;
                const percentChange = (priceChange / previousPrice) * 100;
                
                setCurrentPrice(currentPrice);
                setPriceChange(priceChange);
                setPercentChange(percentChange);
            }
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    };

    useEffect(() => {
        fetchStockData();
    }, [timeframe, ticker]);

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: (context) => {
                        return `${ticker}: $${context.parsed.y.toFixed(2)}`;
                    },
                    title: (tooltipItems) => {
                        return formatDate(tooltipItems[0].label);
                    }
                }
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    maxRotation: 0,
                    autoSkip: true,
                    maxTicksLimit: getTickCount(),
                    callback: (value) => {
                        return formatDate(stockData?.dates[value] || '');
                    }
                }
            },
            y: {
                position: 'right',
                grid: {
                    color: '#f0f0f0',
                },
                ticks: {
                    callback: (value) => {
                        return `$${value.toFixed(2)}`;
                    }
                }
            }
        },
    };

    const chartData = {
        labels: stockData?.dates || [],
        datasets: [
            {
                label: ticker,
                data: stockData?.closing_prices || [],
                borderColor: priceChange && priceChange >= 0 ? '#34D399' : '#EF4444',
                backgroundColor: priceChange && priceChange >= 0 ? '#34D399' : '#EF4444',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.1,
            }
        ],
    };

    const timeframeButtons = [
        { label: '1D', value: '1d' },
        { label: '5D', value: '5d' },
        { label: '1M', value: '1mo' },
        { label: '6M', value: '6mo' },
        { label: 'YTD', value: 'ytd' },
        { label: '1Y', value: '1y' },
        { label: '5Y', value: '5y' },
        { label: 'Max', value: 'max' },
    ];

    return (
        <div className="w-full p-4 bg-white rounded-lg shadow">
            <div className="mb-6">
                <div className="flex items-baseline gap-4">
                    <h2 className="text-2xl font-bold">{ticker}</h2>
                    {currentPrice && (
                        <span className="text-xl">
                            ${currentPrice.toFixed(2)}
                        </span>
                    )}
                    {priceChange && percentChange && (
                        <span className={`text-sm ${priceChange >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                            {priceChange >= 0 ? '+' : ''}${priceChange.toFixed(2)} ({priceChange >= 0 ? '+' : ''}
                            {percentChange.toFixed(2)}%)
                        </span>
                    )}
                </div>
            </div>

            <div className="flex justify-between items-center mb-4">
                <div className="flex gap-2">
                    {timeframeButtons.map((btn) => (
                        <button
                            key={btn.value}
                            onClick={() => setTimeframe(btn.value)}
                            className={`px-3 py-1 rounded ${timeframe === btn.value ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`}
                        >
                            {btn.label}
                        </button>
                    ))}
                </div>
            </div>
            
            <div className="h-[400px]">
                {stockData ? (
                    <Line data={chartData} options={chartOptions} />
                ) : (
                    <div className="flex items-center justify-center h-full">
                        <p>Loading chart...</p>
                    </div>
                )}
            </div>

            {stockData?.key_metrics && (
                <div className="mt-4 grid grid-cols-3 gap-4">
                    {[
                        { key: 'marketCap', title: 'Market Cap' },
                        { key: 'pe', title: 'P/E' },
                        { key: 'priceToSales', title: 'Price to Sales' },
                        { key: '52WeekHigh', title: '52 Week High' },
                        { key: 'forwardPE', title: 'Forward P/E' },
                        { key: 'priceToBook', title: 'Price to Book' },
                        { key: '52WeekLow', title: '52 Week Low' },
                        { key: 'beta', title: 'Beta' },
                    ].map(({ key, title }) => (
                        <div key={key} className="text-sm">
                            <span className="text-gray-500 capitalize">{title}: </span>
                            <span className="font-medium">
                                {stockData.key_metrics[key] === 'N/A' ? 'N/A' : stockData.key_metrics[key]}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default GenerateStockChart;