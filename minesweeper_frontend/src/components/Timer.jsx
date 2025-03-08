import React from 'react';
import './Timer.css';

function Timer({ seconds, isRunning, gameOver, gameWon }) {
    // Format the time as MM:SS
    const formatTime = (totalSeconds) => {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    };
    
    return (
        <div className="timer">
            <div className="timer-icon">
                <span role="img" aria-label="stopwatch">⏱️</span>
            </div>
            <div className="timer-display">{formatTime(seconds)}</div>
        </div>
    );
}

export default Timer; 