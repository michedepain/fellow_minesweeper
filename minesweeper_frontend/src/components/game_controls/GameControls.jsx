import React, { useState } from 'react';
import { createGame } from '../api';
import { useNavigate } from 'react-router-dom';
import './GameControls.css';

function GameControls() {
    const [width, setWidth] = useState(10);
    const [height, setHeight] = useState(10);
    const [mines, setMines] = useState(10);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleCreateGame = async (e) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);
        
        console.log('Creating game with:', { width, height, mines });
        
        // Validate inputs
        if (mines >= width * height) {
            setError('Too many mines for the given board size!');
            setIsLoading(false);
            return;
        }
        
        try {
            const newGame = await createGame(width, height, mines);
            console.log('New game created:', newGame);
            
            if (newGame && newGame.game_id) {
                navigate(`/games/${newGame.game_id}`);
            } else {
                console.error('Game created but no game_id returned:', newGame);
                setError('Game created but no ID returned. Please try again.');
            }
        } catch (err) {
            console.error('Error creating game:', err);
            setError(err.message || 'Failed to create game. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="game-controls">
            <h2>New Game</h2>
            <form onSubmit={handleCreateGame}>
                <div className="form-group">
                    <label htmlFor="width">Width:</label>
                    <input
                        type="number"
                        id="width"
                        value={width}
                        onChange={(e) => setWidth(parseInt(e.target.value) || 1)}
                        min="5"
                        max="30"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="height">Height:</label>
                    <input
                        type="number"
                        id="height"
                        value={height}
                        onChange={(e) => setHeight(parseInt(e.target.value) || 1)}
                        min="5"
                        max="30"
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="mines">Mines:</label>
                    <input
                        type="number"
                        id="mines"
                        value={mines}
                        onChange={(e) => setMines(parseInt(e.target.value) || 1)}
                        min="1"
                        max={width * height - 1}
                    />
                </div>
                <div className="difficulty-info">
                    <span>Difficulty: {getDifficulty(width, height, mines)}</span>
                    <span>Mine Density: {((mines / (width * height)) * 100).toFixed(1)}%</span>
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Creating...' : 'Create Game'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </form>
        </div>
    );
}

// Helper function to determine difficulty based on mine density
function getDifficulty(width, height, mines) {
    const density = mines / (width * height);
    
    if (density < 0.1) return "Easy";
    if (density < 0.15) return "Medium";
    if (density < 0.2) return "Hard";
    return "Expert";
}

export default GameControls;