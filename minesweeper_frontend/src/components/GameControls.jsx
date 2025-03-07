import React, { useState } from 'react';
import { createGame } from '../api';
import { useNavigate } from 'react-router-dom';
import './GameControls.css';

function GameControls() {
    const [width, setWidth] = useState(10);
    const [height, setHeight] = useState(10);
    const [mines, setMines] = useState(10);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleCreateGame = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const newGame = await createGame(width, height, mines);
            console.log('New game created:', newGame);
            navigate(`/games/${newGame.game_id}`);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="game-controls">
            <h2>New Game</h2>
            <form onSubmit={handleCreateGame}>
                <div>
                    <label htmlFor="width">Width:</label>
                    <input
                        type="number"
                        id="width"
                        value={width}
                        onChange={(e) => setWidth(parseInt(e.target.value) || 1)}
                        min="1"
                        max="30"  // Reasonable limits
                    />
                </div>
                <div>
                    <label htmlFor="height">Height:</label>
                    <input
                        type="number"
                        id="height"
                        value={height}
                        onChange={(e) => setHeight(parseInt(e.target.value) || 1)}
                        min="1"
                        max="30"
                    />
                </div>
                <div>
                    <label htmlFor="mines">Mines:</label>
                    <input
                        type="number"
                        id="mines"
                        value={mines}
                        onChange={(e) => setMines(parseInt(e.target.value) || 1)}
                        min="1"

                    />
                </div>
                <button type="submit">Create Game</button>
                {error && <p className="error-message">{error}</p>}
            </form>
        </div>
    );
}

export default GameControls;