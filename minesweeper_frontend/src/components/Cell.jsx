import React from 'react';
import './Cell.css'; // Import the CSS file

function Cell({ value, onClick, gameOver }) {
    let cellContent = '';
    let cellClassName = 'cell';

    if (value !== '') {
        cellClassName += ' revealed';
        if (value === 'M') {
            cellContent = '💣'; // Mine icon
            cellClassName += ' mine';
        } else if (value === '0') {
          cellContent = '';
          cellClassName += ' empty-revealed';
        }
        else {
            cellContent = value;
            cellClassName += ` num-${value}`; // Add class for styling numbers
        }
    } else {
        cellClassName += ' hidden';
    }
     if (gameOver && value === 'M'){
        cellContent = '💣';
        cellClassName += ' mine';
    }

    return (
        <button 
            className={cellClassName} 
            onClick={onClick}
            data-testid="cell"
            aria-label={`Cell ${value ? 'revealed' : 'hidden'} ${value === 'M' ? 'mine' : ''}`}
            type="button"
        >
            {cellContent}
        </button>
    );
}

export default Cell;