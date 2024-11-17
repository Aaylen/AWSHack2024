import React from 'react';
import { createRoot } from 'react-dom/client';
import { GlobalProvider } from './context/GlobalContext';
import App from './App';

// Get the root element
const container = document.getElementById('root');

// Create a root for React 18
const root = createRoot(container);

// Render the app wrapped in GlobalProvider
root.render(
  <React.StrictMode>
    <GlobalProvider>
      <App />
    </GlobalProvider>
  </React.StrictMode>
);