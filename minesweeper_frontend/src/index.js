import React from 'react';
import ReactDOM from 'react-dom/client'; // Correct import for React 18
import App from './App'; // Import your main App component
import './styles.css'; // Import your global styles

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);