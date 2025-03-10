import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { GameWrapper } from '../App';
import * as api from '../api';

jest.mock('../api');

jest.mock('../components/game_board/GameBoard', () => {
  return function MockGameBoard(props) {
    return <div data-testid="game-board">Game Board: {JSON.stringify(props)}</div>;
  };
});


describe('GameWrapper Component', () => {
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

  test('renders game board when game is loaded', async () => {
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
    
    await waitFor(() => {
      expect(screen.getByTestId('game-board')).toBeInTheDocument();
    });
    
    expect(api.getGame).toHaveBeenCalledWith('test-game-id');
  });

  test('shows error message when API call fails', async () => {
    api.getGame.mockRejectedValue(new Error('Failed to load game'));
    
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load game')).toBeInTheDocument();
    });
  });

  test('shows game not found message when game state is null', async () => {
    api.getGame.mockResolvedValue(null);
    
    render(
      <MemoryRouter initialEntries={['/games/test-game-id']}>
        <Routes>
          <Route path="/games/:gameId" element={<GameWrapper />} />
        </Routes>
      </MemoryRouter>
    );
    
    await waitFor(() => {
      expect(screen.getByText('Game not found.')).toBeInTheDocument();
    });
  });
}); 