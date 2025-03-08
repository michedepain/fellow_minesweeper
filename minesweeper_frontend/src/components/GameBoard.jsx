import React, { useState, useEffect, useRef } from 'react';
import Cell from './Cell';
import Timer from './Timer';
import { revealCell } from '../api';
import confetti from 'canvas-confetti';

function GameBoard({ gameId, boardState, gameOver, gameWon, setGameState}) {
    const [prevGameWon, setPrevGameWon] = useState(false);
    const [prevGameOver, setPrevGameOver] = useState(false);
    const [timerRunning, setTimerRunning] = useState(false);
    const [seconds, setSeconds] = useState(0);
    const timerRef = useRef(null);
    const victorySound = useRef(new Audio('https://assets.mixkit.co/sfx/preview/mixkit-winning-chimes-2015.mp3'));
    const gameOverSound = useRef(new Audio('https://assets.mixkit.co/sfx/preview/mixkit-explosion-with-debris-1701.mp3'));

    // Handle timer
    useEffect(() => {
        // Clear any existing timer
        if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
        }
        
        // Start a new timer if the game is running
        if (timerRunning && !gameOver && !gameWon) {
            timerRef.current = setInterval(() => {
                setSeconds(prevSeconds => prevSeconds + 1);
            }, 1000);
        }
        
        // Clean up on unmount
        return () => {
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        };
    }, [timerRunning, gameOver, gameWon]);

    // Start the timer when the board is first loaded
    useEffect(() => {
        if (boardState && !gameOver && !gameWon && !timerRunning) {
            setTimerRunning(true);
        }
    }, [boardState, gameOver, gameWon, timerRunning]);

    // Handle game won state
    useEffect(() => {
        // Only trigger when gameWon changes from false to true
        if (gameWon && !prevGameWon) {
            console.log("Game won! Triggering celebration...");
            
            // Stop the timer
            setTimerRunning(false);
            
            // Play victory sound
            try {
                victorySound.current.volume = 0.5;
                victorySound.current.currentTime = 0;
                victorySound.current.play().catch(e => console.log("Audio play failed:", e));
            } catch (error) {
                console.error("Error playing victory sound:", error);
            }
            
            // Trigger confetti
            try {
                // Configure confetti to use our canvas
                const myConfetti = confetti.create(
                    document.getElementById('confetti-canvas'), 
                    { resize: true, useWorker: true }
                );
                
                // Simple confetti burst
                myConfetti({
                    particleCount: 200,
                    spread: 100,
                    origin: { y: 0.6 }
                });
                
                // Schedule additional bursts
                setTimeout(() => {
                    myConfetti({
                        particleCount: 150,
                        angle: 60,
                        spread: 70,
                        origin: { x: 0, y: 0.6 }
                    });
                }, 500);
                
                setTimeout(() => {
                    myConfetti({
                        particleCount: 150,
                        angle: 120,
                        spread: 70,
                        origin: { x: 1, y: 0.6 }
                    });
                }, 1000);
                
                // Final big burst
                setTimeout(() => {
                    myConfetti({
                        particleCount: 300,
                        spread: 160,
                        origin: { y: 0.5 }
                    });
                }, 1500);
                
                console.log("Confetti launched!");
            } catch (error) {
                console.error("Error launching confetti:", error);
            }
        }
        
        // Update previous game won state
        setPrevGameWon(gameWon);
    }, [gameWon, prevGameWon]);

    // Play game over sound when player hits a mine
    useEffect(() => {
        // Only play sound when gameOver changes from false to true
        if (gameOver && !prevGameOver) {
            // Stop the timer
            setTimerRunning(false);
            
            // Play game over sound
            try {
                gameOverSound.current.volume = 0.5;
                gameOverSound.current.currentTime = 0;
                gameOverSound.current.play().catch(e => console.log("Audio play failed:", e));
            } catch (error) {
                console.error("Error playing game over sound:", error);
            }
        }
        
        // Update previous game over state
        setPrevGameOver(gameOver);
    }, [gameOver, prevGameOver]);

    const handleCellClick = async (row, col) => {
        console.log('gameID', gameId);
        if (gameOver || gameWon) {
            return; // Don't allow clicks if the game is over
        }
        
        // Ensure timer is running after first click
        if (!timerRunning) {
            setTimerRunning(true);
        }
        
        try{
            const updatedGame = await revealCell(gameId, row, col);
            console.log('updatedGame', updatedGame);
            // Make sure gameId is preserved in the updated state
            setGameState(updatedGame);
        }catch(error){
            console.error("Failed to reveal the cell", error)
        }
    };

    if (!boardState) {
        return <div>Loading...</div>;
    }

    return (
        <div className="game-board-container">
            <Timer 
                seconds={seconds}
                isRunning={timerRunning} 
                gameOver={gameOver} 
                gameWon={gameWon} 
            />
            <div className="game-board">
                {boardState.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                        {row.map((cellState, colIndex) => (
                            <Cell
                                key={colIndex}
                                value={cellState}
                                onClick={() => handleCellClick(rowIndex, colIndex)}
                                gameOver={gameOver}
                            />
                        ))}
                    </div>
                ))}
                {gameOver && <div className="game-over-message">Game Over!</div>}
                {gameWon && <div className="game-won-message">You Won!</div>}
            </div>
        </div>
    );
}

export default GameBoard;