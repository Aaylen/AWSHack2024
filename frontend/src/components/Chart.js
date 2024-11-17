// Existing imports
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

// Chart component
const Chart = () => {
    // Your data and options code...
    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [
            {
                label: 'Stock Price',
                data: [150, 200, 180, 220, 300, 250,300],
                borderColor: '#34D399',
                backgroundColor: 'rgba(52, 211, 153, 0.2)',
                fill: true,
            },
        ],
    };

    const options = {
        responsive: true,
        scales: {
            x: { grid: { color: '#374151' }, ticks: { color: '#D1D5DB' } },
            y: { grid: { color: '#374151' }, ticks: { color: '#D1D5DB' } },
        },
        plugins: {
            legend: {
                labels: {
                    color: '#D1D5DB',
                },
            },
        },
    };

    return (
        <div className="chart-container">
            <Line data={data} options={options} />
        </div>
    );
};

export default Chart;