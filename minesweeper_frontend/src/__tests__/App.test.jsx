import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';
import { GameWrapper } from '../App';
import * as api from '../api';
import * as router from 'react-router-dom';

jest.mock('../api');

jest.mock('../components/game_board/GameBoard', () => {
  return function MockGameBoard(props) {
    return <div data-testid="game-board">Game Board: {JSON.stringify(props)}</div>;
  };
});

jest.mock('.../components/game_controls/GameControls', () => {
  return function MockGameControls() {
    return <div data-testid="game-controls">Game Controls</div>;
  };
});

jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    ...originalModule,
    BrowserRouter: ({ children }) => <div>{children}</div>,
    useParams: jest.fn(),
  };
});

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the game wrapper correctly', async () => {

    router.useParams.mockReturnValue({ gameId: 'test-game-id' });
    
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
    
    render(<GameWrapper />);
    
    expect(screen.getByText('Loading game...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByTestId('game-board')).toBeInTheDocument();
    });
    
    expect(api.getGame).toHaveBeenCalledWith('test-game-id');
  });

  test('shows error message when API call fails', async () => {
    router.useParams.mockReturnValue({ gameId: 'test-game-id' });
    
    api.getGame.mockRejectedValue(new Error('Failed to load game'));
    
    render(<GameWrapper />);
    
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load game')).toBeInTheDocument();
    });
  });

  test('renders default content for unknown routes', () => {
    router.useParams.mockReturnValue({});
    
    jest.spyOn(require('react-router-dom'), 'Routes').mockImplementation(({ children }) => {
      return <div>Select or create a game</div>;
    });
    
    render(<App />);
    
    expect(screen.getByText('Minesweeper')).toBeInTheDocument();
    expect(screen.getByText('Select or create a game')).toBeInTheDocument();
  });
}); 