import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import GameBoard from './components/GameBoard';
import GameControls from './components/GameControls';
import { getGame } from './api';
import './styles.css';

export function GameWrapper() {
    const { gameId } = useParams();
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

     useEffect(() => {
         const fetchGameState = async () => {
             setLoading(true);
             setError(null);
             try {
                 const data = await getGame(gameId);
                 setGameState(data);
             } catch (err) {
                 setError(err.message);
             } finally {
                 setLoading(false);
             }
         };

         fetchGameState();
     }, [gameId]);

     if (loading) return <div>Loading game...</div>;
     if (error) return <div>Error: {error}</div>;
     if (!gameState) return <div>Game not found.</div>;


    return (
        <GameBoard
            gameId={gameState.game_id}
            boardState={gameState.board_state}
            gameOver={gameState.game_over}
            gameWon={gameState.game_won}
            setGameState={setGameState} //Pass down setGameState
        />
    );
}



function App() {
    return (
        <Router>
            <div className="App">
                <h1>Minesweeper</h1>
                <GameControls />
                <Routes>
                    <Route path="/games/:gameId" element={<GameWrapper />} />
                    <Route path="/" element={<div>Select or create a game</div>} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;