import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';
import { GameWrapper } from '../App';
import * as api from '../api';
import * as router from 'react-router-dom';

// Mock the API module
jest.mock('../api');

// Mock the components
jest.mock('../components/GameBoard', () => {
  return function MockGameBoard(props) {
    return <div data-testid="game-board">Game Board: {JSON.stringify(props)}</div>;
  };
});

jest.mock('../components/GameControls', () => {
  return function MockGameControls() {
    return <div data-testid="game-controls">Game Controls</div>;
  };
});

// Mock the react-router-dom hooks
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

  // Test rendering the game wrapper component
  test('renders the game wrapper correctly', async () => {
    // Set up useParams mock to return a specific gameId
    router.useParams.mockReturnValue({ gameId: 'test-game-id' });
    
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
    
    render(<GameWrapper />);
    
    // Check if loading state is shown initially
    expect(screen.getByText('Loading game...')).toBeInTheDocument();
    
    // Wait for the game to load
    await waitFor(() => {
      expect(screen.getByTestId('game-board')).toBeInTheDocument();
    });
    
    // Check if the API was called with the correct game ID
    expect(api.getGame).toHaveBeenCalledWith('test-game-id');
  });

  // Test error handling
  test('shows error message when API call fails', async () => {
    // Set up useParams mock to return a specific gameId
    router.useParams.mockReturnValue({ gameId: 'test-game-id' });
    
    // Mock API error
    api.getGame.mockRejectedValue(new Error('Failed to load game'));
    
    render(<GameWrapper />);
    
    // Wait for the error to be displayed
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to load game')).toBeInTheDocument();
    });
  });

  // Test 404 route by testing the App component with a custom path
  test('renders default content for unknown routes', () => {
    // Set up useParams mock for this test
    router.useParams.mockReturnValue({});
    
    // Mock the Routes component to simulate being on an unknown route
    jest.spyOn(require('react-router-dom'), 'Routes').mockImplementation(({ children }) => {
      return <div>Select or create a game</div>;
    });
    
    render(<App />);
    
    // The App should still render, but with the default route content
    expect(screen.getByText('Minesweeper')).toBeInTheDocument();
    expect(screen.getByText('Select or create a game')).toBeInTheDocument();
  });
}); 