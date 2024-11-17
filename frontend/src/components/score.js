import React from 'react';
import PropTypes from 'prop-types';  // Optional, for type checking
import './score.css';  // Import the CSS file

const Score = ({ score }) => {
  // Ensure the score is a valid number and convert to a valid percentage
  const formattedScore = isNaN(score) ? 'Invalid Score' : score;
  
  // Determine the text to display
  let label = "Hold";
  let labelStyle = { color: 'gray' };
  if (score > 70) {
    label = "Bullish";
    labelStyle = { color: 'green' };
  } else if (score < 40) {
    label = "Bearish";
    labelStyle = { color: 'red' };
  }

  // Calculate the dot position as a percentage
  const dotPosition = score < 0 ? 0 : score > 100 ? 100 : score;

  return (
    <div className="score-display">
      
      <div className="line-container">
        <div className="gradient-line">
          <div
            className="score-dot"
            style={{ left: `${dotPosition}%` }}
          ></div>
        </div>
        <div className="label" style={labelStyle}>
          {label}
        </div>
      </div>
    </div>
  );
};

Score.propTypes = {
  score: PropTypes.number.isRequired
};

export default Score;
