import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { GameWrapper } from '../App';
import * as api from '../api';

// Mock the API module
jest.mock('../api');

// Mock the GameBoard component
jest.mock('../components/GameBoard', () => {
  return function MockGameBoard(props) {
    return <div data-testid="game-board">Game Board: {JSON.stringify(props)}</div>;
  };
});

// We need to export GameWrapper from App.js for this test to work
// If it's not exported, we'll need to modify App.js to export it

describe('GameWrapper Component', () => {
  // Test loading state
  test('shows loading state initially', () => {
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    expect(screen.getByText('Loading game...')).toBeInTheDocument();
  });

  // Test successful game loading
  test('renders game board when game is loaded', async () => {
    // Mock the API response
    const mockGame = {
      game_id: 'test-game-id',
      width: 10,
      height: 10,
      mines: 10,
      board_state: [['', '', ''], ['', '', '']],
      game_over: false,
      game_won: false
    };
    
    api.getGame.mockResolvedValue(mockGame);
    
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByTestId('game-board')).toBeInTheDocument();
    });
    
    // Check if the API was called with the correct game ID
    expect(api.getGame).toHaveBeenCalledWith('test-game-id');
  });

  // Test error handling
  test('shows error message when API call fails', async () => {
    // Mock API error
    api.getGame.mockRejectedValue(new Error('Failed to load game'));
    
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    // Wait for the error to be displayed
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load game')).toBeInTheDocument();
    });
  });

  // Test game not found
  test('shows game not found message when game state is null', async () => {
    // Mock API returning null
    api.getGame.mockResolvedValue(null);
    
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    // Wait for the not found message to be displayed
    await waitFor(() => {
      expect(screen.getByText('Game not found.')).toBeInTheDocument();
    });
  });
}); 