import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import GameBoard from '../GameBoard';
import * as api from '../../api';

// Mock the API module
jest.mock('../../api');

describe('GameBoard Component', () => {
  // Sample board state for testing
  const mockBoardState = [
    ['', '1', ''],
    ['', '2', ''],
    ['', '', '']
  ];
  
  // Reset mocks before each test
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Test rendering the game board
  test('renders the game board correctly', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={false} 
        gameWon={false} 
        setGameState={() => {}}
      />
    );
    
    // Check if the correct number of cells are rendered
    const cells = screen.getAllByTestId('cell');
    expect(cells).toHaveLength(9); // 3x3 board
    
    // Check if the revealed cells show their values
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  // Test loading state
  test('shows loading state when boardState is null', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={null} 
        gameOver={false} 
        gameWon={false} 
        setGameState={() => {}}
      />
    );
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  // Test game over message
  test('shows game over message when gameOver is true', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={true} 
        gameWon={false} 
        setGameState={() => {}}
      />
    );
    
    expect(screen.getByText('Game Over!')).toBeInTheDocument();
  });

  // Test game won message
  test('shows game won message when gameWon is true', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={false} 
        gameWon={true} 
        setGameState={() => {}}
      />
    );
    
    expect(screen.getByText('You Won!')).toBeInTheDocument();
  });

  // Test cell click
  test('calls revealCell API and updates state when a cell is clicked', async () => {
    // Mock the API response
    const mockUpdatedGame = {
      game_id: 'test-id',
      board_state: [
        ['0', '1', ''],
        ['0', '2', ''],
        ['', '', '']
      ],
      game_over: false,
      game_won: false
    };
    
    api.revealCell.mockResolvedValue(mockUpdatedGame);
    
    const setGameStateMock = jest.fn();
    
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={false} 
        gameWon={false} 
        setGameState={setGameStateMock}
      />
    );
    
    // Click on a hidden cell (first cell in the first row)
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    // Check if the API was called with correct parameters
    expect(api.revealCell).toHaveBeenCalledWith('test-id', 0, 0);
    
    // Wait for the state to be updated
    await waitFor(() => {
      expect(setGameStateMock).toHaveBeenCalledWith(mockUpdatedGame);
    });
  });

  // Test that clicking is disabled when game is over
  test('does not call API when game is over', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={true} 
        gameWon={false} 
        setGameState={() => {}}
      />
    );
    
    // Click on a cell
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    // API should not be called
    expect(api.revealCell).not.toHaveBeenCalled();
  });

  // Test that clicking is disabled when game is won
  test('does not call API when game is won', () => {
    render(
      <GameBoard 
        gameId="test-id" 
        boardState={mockBoardState} 
        gameOver={false} 
        gameWon={true} 
        setGameState={() => {}}
      />
    );
    
    // Click on a cell
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    // API should not be called
    expect(api.revealCell).not.toHaveBeenCalled();
  });
}); 