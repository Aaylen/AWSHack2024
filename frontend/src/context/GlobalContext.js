// src/context/GlobalContext.js
import React, { createContext, useContext, useState } from 'react';

// Create the context
const GlobalContext = createContext();

// Provider component
export function GlobalProvider({ children }) {
    const [ticker, setTicker] = useState('SPY');
    const [score, setScore] = useState(90);

    const value = {
        ticker,
        setTicker,
        score,      // Add score to the context value
        setScore    // Add setScore to the context value
    };

    return (
        <GlobalContext.Provider value={value}>
            {children}
        </GlobalContext.Provider>
    );
}

// Custom hook for using the global context
export function useGlobal() {
    const context = useContext(GlobalContext);
    if (context === undefined) {
        throw new Error('useGlobal must be used within a GlobalProvider');
    }
    return context;
}

export default GlobalContext;
