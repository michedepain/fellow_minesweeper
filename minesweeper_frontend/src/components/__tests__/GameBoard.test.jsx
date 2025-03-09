import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import GameBoard from '../GameBoard';
import * as api from '../../api';

jest.mock('../../api');

describe('GameBoard Component', () => {
  const mockBoardState = [
    ['', '1', ''],
    ['', '2', ''],
    ['', '', '']
  ];
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

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
    
    const cells = screen.getAllByTestId('cell');
    expect(cells).toHaveLength(9);
    
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

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

  test('calls revealCell API and updates state when a cell is clicked', async () => {
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
    
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    expect(api.revealCell).toHaveBeenCalledWith('test-id', 0, 0);
    
    await waitFor(() => {
      expect(setGameStateMock).toHaveBeenCalledWith(mockUpdatedGame);
    });
  });

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
    
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    expect(api.revealCell).not.toHaveBeenCalled();
  });

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
    
    const cells = screen.getAllByTestId('cell');
    fireEvent.click(cells[0]);
    
    expect(api.revealCell).not.toHaveBeenCalled();
  });
}); 