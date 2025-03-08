import { createGame, getGame, revealCell } from '../api';

// Mock fetch globally
global.fetch = jest.fn();

describe('API Functions', () => {
  // Setup before each test
  beforeEach(() => {
    // Reset mocks
    fetch.mockClear();
  });

  // Test createGame function
  describe('createGame', () => {
    test('calls fetch with correct parameters', async () => {
      // Mock successful response
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          game_id: 'test-id',
          width: 10,
          height: 10,
          mines: 10,
          board_state: []
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      const result = await createGame(10, 10, 10);
      
      // Check if fetch was called correctly
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/games/'),
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ width: 10, height: 10, mines: 10 }),
        }
      );
      
      // Check if response was processed correctly
      expect(mockResponse.json).toHaveBeenCalled();
      expect(result).toEqual({
        game_id: 'test-id',
        width: 10,
        height: 10,
        mines: 10,
        board_state: []
      });
    });
    
    test('throws error when response is not ok', async () => {
      // Mock error response
      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Failed to create game'
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function and expect it to throw
      await expect(createGame(10, 10, 10)).rejects.toThrow('Failed to create game');
    });
  });

  // Test getGame function
  describe('getGame', () => {
    test('calls fetch with correct parameters', async () => {
      // Mock successful response
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          game_id: 'test-id',
          width: 10,
          height: 10,
          mines: 10,
          board_state: []
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      const result = await getGame('test-id');
      
      // Check if fetch was called correctly
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/games/test-id/')
      );
      
      // Check if response was processed correctly
      expect(mockResponse.json).toHaveBeenCalled();
      expect(result).toEqual({
        game_id: 'test-id',
        width: 10,
        height: 10,
        mines: 10,
        board_state: []
      });
    });
    
    test('throws error when response is not ok', async () => {
      // Mock error response
      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Game not found'
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function and expect it to throw
      await expect(getGame('test-id')).rejects.toThrow('Game not found');
    });
  });

  // Test revealCell function
  describe('revealCell', () => {
    test('calls fetch with correct parameters', async () => {
      // Mock successful response
      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          game_id: 'test-id',
          board_state: [['0', '1', ''], ['', '', '']],
          game_over: false,
          game_won: false
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function
      const result = await revealCell('test-id', 0, 0);
      
      // Check if fetch was called correctly
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/games/test-id/reveal/'),
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ row: 0, col: 0 }),
        }
      );
      
      // Check if response was processed correctly
      expect(mockResponse.json).toHaveBeenCalled();
      expect(result).toEqual({
        game_id: 'test-id',
        board_state: [['0', '1', ''], ['', '', '']],
        game_over: false,
        game_won: false
      });
    });
    
    test('throws error when response is not ok', async () => {
      // Mock error response
      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Failed to reveal cell'
        })
      };
      
      fetch.mockResolvedValue(mockResponse);
      
      // Call the function and expect it to throw
      await expect(revealCell('test-id', 0, 0)).rejects.toThrow('Failed to reveal cell');
    });
  });
}); 