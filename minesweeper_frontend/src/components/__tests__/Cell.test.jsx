import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Cell from '../Cell';

describe('Cell Component', () => {
  // Test rendering a hidden cell
  test('renders a hidden cell correctly', () => {
    const onClick = jest.fn();
    render(<Cell value="" onClick={onClick} gameOver={false} />);
    
    const cellElement = screen.getByTestId('cell');
    expect(cellElement).toHaveClass('cell');
    expect(cellElement).toHaveClass('hidden');
    expect(cellElement).not.toHaveClass('revealed');
    expect(cellElement).toBeEmptyDOMElement();
  });

  // Test rendering a revealed cell with a number
  test('renders a revealed cell with a number correctly', () => {
    const onClick = jest.fn();
    render(<Cell value="3" onClick={onClick} gameOver={false} />);
    
    const cellElement = screen.getByText('3');
    expect(cellElement).toHaveClass('cell');
    expect(cellElement).toHaveClass('revealed');
    expect(cellElement).toHaveClass('num-3');
    expect(cellElement).not.toHaveClass('hidden');
  });

  // Test rendering a revealed cell with a mine
  test('renders a revealed cell with a mine correctly', () => {
    const onClick = jest.fn();
    render(<Cell value="M" onClick={onClick} gameOver={false} />);
    
    const cellElement = screen.getByText('💣');
    expect(cellElement).toHaveClass('cell');
    expect(cellElement).toHaveClass('revealed');
    expect(cellElement).toHaveClass('mine');
    expect(cellElement).not.toHaveClass('hidden');
  });

  // Test rendering a revealed empty cell (value "0")
  test('renders a revealed empty cell correctly', () => {
    const onClick = jest.fn();
    render(<Cell value="0" onClick={onClick} gameOver={false} />);
    
    const cellElement = screen.getByTestId('cell');
    expect(cellElement).toHaveClass('cell');
    expect(cellElement).toHaveClass('revealed');
    expect(cellElement).toHaveClass('empty-revealed');
    expect(cellElement).not.toHaveClass('hidden');
    expect(cellElement).toBeEmptyDOMElement();
  });

  // Test clicking a cell
  test('calls onClick when cell is clicked', () => {
    const onClick = jest.fn();
    render(<Cell value="" onClick={onClick} gameOver={false} />);
    
    const cellElement = screen.getByTestId('cell');
    fireEvent.click(cellElement);
    
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  // Test game over state with a mine
  test('shows mine when game is over', () => {
    const onClick = jest.fn();
    render(<Cell value="M" onClick={onClick} gameOver={true} />);
    
    const cellElement = screen.getByText('💣');
    expect(cellElement).toHaveClass('mine');
  });
}); 