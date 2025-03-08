import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import GameControls from '../GameControls';
import * as api from '../../api';
import * as router from 'react-router-dom';

// Mock the API module
jest.mock('../../api');

// Mock the useNavigate hook
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn()
}));

describe('GameControls Component', () => {
  // Setup before each test
  beforeEach(() => {
    // Reset mocks
    api.createGame.mockReset();
    router.useNavigate.mockReset();
    
    // Setup default mock for useNavigate
    const navigateMock = jest.fn();
    router.useNavigate.mockReturnValue(navigateMock);
  });

  // Test rendering the form
  test('renders the game controls form correctly', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    // Check if form elements are rendered
    expect(screen.getByLabelText(/width/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/height/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/mines/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create game/i })).toBeInTheDocument();
  });

  // Test form input changes
  test('updates state when form inputs change', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    // Get form inputs
    const widthInput = screen.getByLabelText(/width/i);
    const heightInput = screen.getByLabelText(/height/i);
    const minesInput = screen.getByLabelText(/mines/i);
    
    // Change input values
    fireEvent.change(widthInput, { target: { value: '15' } });
    fireEvent.change(heightInput, { target: { value: '20' } });
    fireEvent.change(minesInput, { target: { value: '30' } });
    
    // Check if inputs have new values
    expect(widthInput.value).toBe('15');
    expect(heightInput.value).toBe('20');
    expect(minesInput.value).toBe('30');
  });

  // Test form submission
  test('calls createGame API and navigates on form submission', async () => {
    // Mock the API response
    const mockGame = {
      game_id: 'test-game-id',
      width: 10,
      height: 10,
      mines: 10,
      board_state: []
    };
    
    api.createGame.mockResolvedValue(mockGame);
    
    const navigateMock = jest.fn();
    router.useNavigate.mockReturnValue(navigateMock);
    
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /create game/i });
    fireEvent.click(submitButton);
    
    // Check if the API was called with default values
    expect(api.createGame).toHaveBeenCalledWith(10, 10, 10);
    
    // Wait for navigation to happen
    await waitFor(() => {
      expect(navigateMock).toHaveBeenCalledWith('/games/test-game-id');
    });
  });

  // Test error handling
  test('displays error message when API call fails', async () => {
    // Mock API error
    api.createGame.mockRejectedValue(new Error('Failed to create game'));
    
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /create game/i });
    fireEvent.click(submitButton);
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to create game')).toBeInTheDocument();
    });
  });

  // Test form validation
  test('prevents invalid input values', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    // Get form inputs
    const widthInput = screen.getByLabelText(/width/i);
    const heightInput = screen.getByLabelText(/height/i);
    const minesInput = screen.getByLabelText(/mines/i);
    
    // Try to set invalid values
    fireEvent.change(widthInput, { target: { value: '-5' } });
    fireEvent.change(heightInput, { target: { value: '0' } });
    
    // Check if inputs have valid values (min should be enforced)
    expect(widthInput).toHaveAttribute('min', '1');
    expect(heightInput).toHaveAttribute('min', '1');
    expect(minesInput).toHaveAttribute('min', '1');
  });
}); 