import React, { useState, useEffect, useRef } from 'react';
import Cell from '../cell/Cell';
import Timer from '../timer/Timer';
import { revealCell } from '../../api';
import confetti from 'canvas-confetti';

function GameBoard({ gameId, boardState, gameOver, gameWon, setGameState}) {
    const [prevGameWon, setPrevGameWon] = useState(false);
    const [prevGameOver, setPrevGameOver] = useState(false);
    const [timerRunning, setTimerRunning] = useState(false);
    const [seconds, setSeconds] = useState(0);
    const timerRef = useRef(null);
    const victorySound = useRef(new Audio('https://assets.mixkit.co/sfx/preview/mixkit-winning-chimes-2015.mp3'));
    const gameOverSound = useRef(new Audio('https://assets.mixkit.co/sfx/preview/mixkit-explosion-with-debris-1701.mp3'));

    useEffect(() => {
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
            
            setTimerRunning(false);
            
            try {
                victorySound.current.volume = 0.5;
                victorySound.current.currentTime = 0;
                victorySound.current.play().catch(e => console.log("Audio play failed:", e));
            } catch (error) {
                console.error("Error playing victory sound:", error);
            }
            
            try {
                const myConfetti = confetti.create(
                    document.getElementById('confetti-canvas'), 
                    { resize: true, useWorker: true }
                );
                
                myConfetti({
                    particleCount: 200,
                    spread: 100,
                    origin: { y: 0.6 }
                });
                
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
        
        setPrevGameWon(gameWon);
    }, [gameWon, prevGameWon]);

    useEffect(() => {
        if (gameOver && !prevGameOver) {
            setTimerRunning(false);
            
            try {
                gameOverSound.current.volume = 0.5;
                gameOverSound.current.currentTime = 0;
                gameOverSound.current.play().catch(e => console.log("Audio play failed:", e));
            } catch (error) {
                console.error("Error playing game over sound:", error);
            }
        }
        
        setPrevGameOver(gameOver);
    }, [gameOver, prevGameOver]);

    const handleCellClick = async (row, col) => {
        console.log('gameID', gameId);
        if (gameOver || gameWon) {
            return;
        }
        
        if (!timerRunning) {
            setTimerRunning(true);
        }
        
        try{
            const updatedGame = await revealCell(gameId, row, col);
            console.log('updatedGame', updatedGame);
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