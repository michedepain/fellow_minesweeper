import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams, useNavigate, Navigate } from 'react-router-dom';
import GameBoard from './components/game_board/GameBoard';
import GameControls from './game_controls/GameControls';
import { getGame } from './api';
import './styles.css';

export function GameWrapper() {
    const { gameId } = useParams();
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

     useEffect(() => {
         const fetchGameState = async () => {
             // Check if gameId is valid
             if (!gameId) {
                 console.error('No gameId provided');
                 setError('No game ID provided');
                 setLoading(false);
                 return;
             }
             
             console.log('Fetching game state for ID:', gameId);
             setLoading(true);
             setError(null);
             
             try {
                 const data = await getGame(gameId);
                 console.log('Game data received:', data);
                 setGameState(data);
             } catch (err) {
                 console.error('Error fetching game:', err);
                 setError(err.message || 'Failed to load game');
             } finally {
                 setLoading(false);
             }
         };

         fetchGameState();
     }, [gameId]);

     const handleNewGame = () => {
         navigate('/');
     };

     if (loading) return <div className="loading-container"><div>Loading game...</div></div>;
     if (error) return <div className="error-container"><div>Error: {error}</div><button onClick={handleNewGame}>New Game</button></div>;
     if (!gameState) return <div className="not-found-container"><div>Game not found.</div><button onClick={handleNewGame}>New Game</button></div>;

    return (
        <div className="game-page">
            <h1>Minesweeper</h1>
            <div className="game-actions">
                <button onClick={handleNewGame} className="new-game-button">New Game</button>
            </div>
            <GameBoard
                gameId={gameState.game_id}
                boardState={gameState.board_state}
                gameOver={gameState.game_over}
                gameWon={gameState.game_won}
                setGameState={setGameState}
            />
        </div>
    );
}

function HomePage() {
    return (
        <div className="home-page">
            <h1>Minesweeper</h1>
            <GameControls />
        </div>
    );
}

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/games/:gameId" element={<GameWrapper />} />
                    <Route path="/games" element={<Navigate to="/" replace />} />
                    <Route path="/" element={<HomePage />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;