import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import GameControls from '../GameControls';
import * as api from '../../api';
import * as router from 'react-router-dom';

jest.mock('../../api');

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn()
}));

describe('GameControls Component', () => {
  beforeEach(() => {
    api.createGame.mockReset();
    router.useNavigate.mockReset();
    
    const navigateMock = jest.fn();
    router.useNavigate.mockReturnValue(navigateMock);
  });

  test('renders the game controls form correctly', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    expect(screen.getByLabelText(/width/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/height/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/mines/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create game/i })).toBeInTheDocument();
  });

  test('updates state when form inputs change', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    const widthInput = screen.getByLabelText(/width/i);
    const heightInput = screen.getByLabelText(/height/i);
    const minesInput = screen.getByLabelText(/mines/i);
    
    fireEvent.change(widthInput, { target: { value: '15' } });
    fireEvent.change(heightInput, { target: { value: '20' } });
    fireEvent.change(minesInput, { target: { value: '30' } });
    
    expect(widthInput.value).toBe('15');
    expect(heightInput.value).toBe('20');
    expect(minesInput.value).toBe('30');
  });

  test('calls createGame API and navigates on form submission', async () => {
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
    
    const submitButton = screen.getByRole('button', { name: /create game/i });
    fireEvent.click(submitButton);
    
    expect(api.createGame).toHaveBeenCalledWith(10, 10, 10);
    
    await waitFor(() => {
      expect(navigateMock).toHaveBeenCalledWith('/games/test-game-id');
    });
  });

  test('displays error message when API call fails', async () => {
    api.createGame.mockRejectedValue(new Error('Failed to create game'));
    
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    const submitButton = screen.getByRole('button', { name: /create game/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to create game')).toBeInTheDocument();
    });
  });

  test('prevents invalid input values', () => {
    render(
      <MemoryRouter>
        <GameControls />
      </MemoryRouter>
    );
    
    const widthInput = screen.getByLabelText(/width/i);
    const heightInput = screen.getByLabelText(/height/i);
    const minesInput = screen.getByLabelText(/mines/i);
    
    fireEvent.change(widthInput, { target: { value: '-5' } });
    fireEvent.change(heightInput, { target: { value: '0' } });
    
    expect(widthInput).toHaveAttribute('min', '1');
    expect(heightInput).toHaveAttribute('min', '1');
    expect(minesInput).toHaveAttribute('min', '1');
  });
}); 