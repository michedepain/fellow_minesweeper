import random
import logging
from functools import lru_cache

from minesweeper_backend.models import Game

logger = logging.getLogger(__name__)

def generate_minesweeper_board(width, height, mines):
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
    
    return {
        'internal_board': internal_board,
        'player_board': player_board
    }


def reveal_cell(board, row, col, internal_board=None, game=None):
    """
    Reveals a cell on the game board.
    
    Args:
        board: The player's board to update
        row: Row index of the cell to reveal
        col: Column index of the cell to reveal
        internal_board: Optional internal board to avoid database lookup
        game: Optional game object to avoid database lookup
        
    Returns:
        -1: If a mine was revealed (game over)
         0: If no cell was revealed (out of bounds, already revealed, or game not found)
         n: Number of cells revealed (n > 0)
    """
    # Track the number of cells revealed in this operation
    cells_revealed = 0
    
    # Use a stack instead of recursion to avoid stack overflow for large boards
    stack = [(row, col)]
    visited = set()
    
    # Early return if the cell is invalid
    if not is_valid_cell_simple(board, row, col):
        logger.debug(f"Invalid cell: ({row}, {col})")
        return 0
    
    # Get the game and internal board if not provided
    if not game:
        game = get_game_from_board(board)
        if not game:
            logger.debug("Game not found")
            return 0
    
    if not internal_board:
        internal_board = game.internal_board
    
    # Process cells using a stack-based approach
    while stack:
        current_row, current_col = stack.pop()
        
        # Skip if already visited or invalid
        if (current_row, current_col) in visited or not is_valid_cell_simple(board, current_row, current_col):
            continue
        
        # Skip if already revealed
        if board[current_row][current_col] != '':
            continue
        
        # Mark as visited
        visited.add((current_row, current_col))
        
        # Check if it's a mine
        if internal_board[current_row][current_col] == 'M':
            board[current_row][current_col] = 'M'
            return -1
        
        # Count adjacent mines
        mine_count = count_adjacent_mines_simple(internal_board, current_row, current_col)
        board[current_row][current_col] = str(mine_count) if mine_count > 0 else '0'
        cells_revealed += 1
        
        # If no adjacent mines, add neighboring cells to the stack
        if mine_count == 0:
            height = len(board)
            width = len(board[0]) if height > 0 else 0
            
            for i in range(max(0, current_row-1), min(height, current_row+2)):
                for j in range(max(0, current_col-1), min(width, current_col+2)):
                    # Skip the current cell
                    if i == current_row and j == current_col:
                        continue
                    
                    # Skip already revealed or visited cells
                    if board[i][j] != '' or (i, j) in visited:
                        continue
                    
                    # Add to stack
                    stack.append((i, j))
    
    return cells_revealed


# Simple version without caching for direct use with lists
def is_valid_cell_simple(board, row, col):
    """Check if the cell coordinates are within the board boundaries."""
    try:
        height = len(board)
        width = len(board[0]) if height > 0 else 0
        return 0 <= row < height and 0 <= col < width
    except (TypeError, IndexError):
        return False


# Cached version that converts board to a hashable tuple
def is_valid_cell(board, row, col):
    """Check if the cell coordinates are within the board boundaries."""
    # Convert board to a hashable type (tuple of tuples)
    try:
        board_tuple = tuple(tuple(row) for row in board)
        return _is_valid_cell_cached(board_tuple, row, col)
    except (TypeError, IndexError):
        return False


@lru_cache(maxsize=128)
def _is_valid_cell_cached(board_tuple, row, col):
    """Cached version that works with hashable board representation."""
    try:
        height = len(board_tuple)
        width = len(board_tuple[0]) if height > 0 else 0
        return 0 <= row < height and 0 <= col < width
    except (TypeError, IndexError):
        return False


def get_game_from_board(board):
    """Retrieve the Game object associated with the given player board."""
    return Game.objects.filter(player_board=board).first()


# Simple version without caching for direct use with lists
def count_adjacent_mines_simple(board, row, col):
    """Count the number of mines adjacent to the given cell."""
    count = 0
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    
    for i in range(max(0, row-1), min(height, row+2)):
        for j in range(max(0, col-1), min(width, col+2)):
            if i == row and j == col:
                continue  # Skip the cell itself
            if board[i][j] == 'M':
                count += 1
    return count


# Cached version that converts board to a hashable tuple
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
    # Convert board to a hashable type (tuple of tuples)
    try:
        board_tuple = tuple(tuple(row) for row in board)
        return _count_adjacent_mines_cached(board_tuple, row, col)
    except (TypeError, IndexError):
        return 0


@lru_cache(maxsize=1024)
def _count_adjacent_mines_cached(board_tuple, row, col):
    """Cached version that works with hashable board representation."""
    count = 0
    height = len(board_tuple)
    width = len(board_tuple[0]) if height > 0 else 0
    
    for i in range(max(0, row-1), min(height, row+2)):
        for j in range(max(0, col-1), min(width, col+2)):
            if i == row and j == col:
                continue  # Skip the cell itself
            if board_tuple[i][j] == 'M':
                count += 1
    return count