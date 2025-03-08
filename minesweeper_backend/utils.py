import random
import logging

from minesweeper_backend.models import Game

# Set up logging
logger = logging.getLogger(__name__)

def generate_minesweeper_board(width, height, mines):
    # Create the internal board with mines placed
    internal_board = [['' for _ in range(width)] for _ in range(height)]
    mines_placed = 0

    while mines_placed < mines:
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        if internal_board[x][y] != 'M':
            internal_board[x][y] = 'M'
            mines_placed += 1
    
    # Create the player's view board (all cells hidden)
    player_board = [['' for _ in range(width)] for _ in range(height)]
    
    # Return both boards - internal board for game logic, player board for display
    return {
        'internal_board': internal_board,
        'player_board': player_board
    }


def reveal_cell(board, row, col):
    """
    Reveals a cell on the game board.
    
    Args:
        board: The player's board to update
        row: Row index of the cell to reveal
        col: Column index of the cell to reveal
        
    Returns:
        -1: If a mine was revealed (game over)
         0: If no cell was revealed (out of bounds, already revealed, or game not found)
         1: If a cell was successfully revealed
    """
    # Early return if the cell is invalid or already revealed
    if not is_valid_cell(board, row, col) or board[row][col] != '':
        return 0
    
    # Get the game associated with this board
    game = get_game_from_board(board)
    if not game:
        return 0
    
    internal_board = game.internal_board
    
    # Handle mine cell
    if internal_board[row][col] == 'M':
        board[row][col] = 'M'  # Reveal the mine
        return -1  # Game over
    
    # Count adjacent mines and update the cell
    mine_count = count_adjacent_mines(internal_board, row, col)
    board[row][col] = str(mine_count) if mine_count > 0 else '0'
    
    # Auto-reveal adjacent cells if no mines are nearby
    if mine_count == 0:
        # Get the dimensions of the board
        height = len(board)
        width = len(board[0]) if height > 0 else 0
        
        # Check all adjacent cells
        for i in range(max(0, row-1), min(height, row+2)):
            for j in range(max(0, col-1), min(width, col+2)):
                # Skip the current cell
                if i == row and j == col:
                    continue
                
                # Skip already revealed cells
                if board[i][j] != '':
                    continue
                
                reveal_cell(board, i, j)
    
    return 1  # Cell successfully revealed


def is_valid_cell(board, row, col):
    """Check if the cell coordinates are within the board boundaries."""
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_game_from_board(board):
    """Retrieve the Game object associated with the given player board."""
    return Game.objects.filter(player_board=board).first()


def count_adjacent_mines(board, row, col):
    """
    Count the number of mines adjacent to the given cell.
    
    Args:
        board: The board containing mine positions (internal board)
        row: Row index of the cell
        col: Column index of the cell
        
    Returns:
        Number of adjacent mines
    """
    count = 0
    for i in range(max(0, row-1), min(len(board), row+2)):
        for j in range(max(0, col-1), min(len(board[0]), col+2)):
            if i == row and j == col:
                continue  # Skip the cell itself
            if board[i][j] == 'M':
                count += 1
    return count