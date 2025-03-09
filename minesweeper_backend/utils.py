import random
import logging
from functools import lru_cache

from minesweeper_backend.models import Game

logger = logging.getLogger(__name__)

def generate_minesweeper_board(width, height, mines):
    """
    Generates a new Minesweeper board with randomly placed mines.
    
    Args:
        width: Width of the board (number of columns)
        height: Height of the board (number of rows)
        mines: Number of mines to place on the board
        
    Returns:
        Dictionary containing:
        - 'internal_board': 2D list with mine positions (visible only to the system)
        - 'player_board': 2D list with all cells hidden (what the player sees)
        
    Example:
        generate_minesweeper_board(3, 3, 2) might return:
        {
            'internal_board': [
                ['', '', 'M'],
                ['', '', ''],
                ['M', '', '']
            ],
            'player_board': [
                ['', '', ''],
                ['', '', ''],
                ['', '', '']
            ]
        }
        
        Where 'M' represents a mine and '' represents an empty cell.
        The player_board starts with all cells hidden ('').
    """
    internal_board = [['' for _ in range(width)] for _ in range(height)]
    mines_placed = 0

    while mines_placed < mines:
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        
        # Only place a mine if the cell doesn't already have one
        if internal_board[x][y] != 'M':
            internal_board[x][y] = 'M'
            mines_placed += 1
    
    # Create an empty board with the specified dimensions
    player_board = [
        ['' for _ in range(width)]
        for _ in range(height)
    ]

    return {
        'internal_board': internal_board,
        'player_board': player_board
    }


def reveal_cell(board, row, col, internal_board=None, game=None):
    """
    Reveals a cell on the game board and automatically reveals adjacent empty cells.
    Uses an iterative approach with a stack to avoid stack overflow on large boards.
    
    Args:
        board: The player's visible board to update (e.g., [['', '', ''], ['', '', ''], ...])
        row: Row index of the cell to reveal (0-based)
        col: Column index of the cell to reveal (0-based)
        internal_board: Optional internal board with mine positions to avoid database lookup
        game: Optional game object to avoid database lookup
        
    Returns:
        -1: If a mine was revealed (game over)
         0: If no cell was revealed (out of bounds, already revealed, or game not found)
         n: Number of cells revealed (n > 0)
    
    Example:
        Starting with player_board = [['', '', ''], ['', '', ''], ['', '', 'M']]
        and internal_board = [['', '', ''], ['', '', ''], ['', '', 'M']]
        
        reveal_cell(player_board, 0, 0) would update player_board to:
        [['0', '0', '0'], ['0', '1', '1'], ['0', '1', '']]
        
        and return 8 (the number of cells revealed)
    """
    # Track the number of cells revealed in this operation
    cells_revealed = 0
    
    # Use a stack to keep track of cells to process
    # We start with the initial cell the player clicked
    stack = [(row, col)]
    
    # Keep track of cells we've already considered to avoid duplicates
    visited = set()
    
    # Step 1: Validate the initial cell coordinates
    if not is_valid_cell_simple(board, row, col):
        logger.debug(f"Invalid cell coordinates: ({row}, {col})")
        return 0
    
    # Step 2: Get the game and internal board if not provided
    if not game:
        game = get_game_from_board(board)
        if not game:
            logger.debug("Game not found in database")
            return 0
    
    if not internal_board:
        internal_board = game.internal_board
    
    # Step 3: Continue processing cells until the stack is empty
    while stack:
        current_row, current_col = stack.pop()
        
        if (current_row, current_col) in visited or not is_valid_cell_simple(board, current_row, current_col):
            continue
        
        if board[current_row][current_col] != '':
            continue
        
        visited.add((current_row, current_col))
        
        # Step 4: Check if it's a mine
        if internal_board[current_row][current_col] == 'M':
            board[current_row][current_col] = 'M'
            return -1  # Game over!
        
        # Step 5: Count adjacent mines and update the cell
        mine_count = count_adjacent_mines_simple(internal_board, current_row, current_col)
        
        # Update the player's board with the count (or '0' for empty cells)
        board[current_row][current_col] = str(mine_count) if mine_count > 0 else '0'
        cells_revealed += 1
        
        # Step 6: If the current cell has no adjacent mines, reveal all adjacent cells
        if mine_count == 0:
            height = len(board)
            width = len(board[0]) if height > 0 else 0
            
            # Check all 8 adjacent cells (horizontally, vertically, and diagonally)
            for i in range(max(0, current_row-1), min(height, current_row+2)):
                for j in range(max(0, current_col-1), min(width, current_col+2)):

                    if i == current_row and j == current_col:
                        continue
                    
                    if board[i][j] != '' or (i, j) in visited:
                        continue
                    
                    stack.append((i, j))
                    
    return cells_revealed


# Simple version without caching for direct use with lists
def is_valid_cell_simple(board, row, col):
    """
    Checks if the cell coordinates are within the board boundaries.
    This is a simple version that works directly with list boards.
    
    Args:
        board: The game board as a 2D list
        row: Row index to check
        col: Column index to check
        
    Returns:
        True if the coordinates are valid, False otherwise
        
    Example:
        For a 3x3 board, valid coordinates are (0,0) through (2,2)
        is_valid_cell_simple(board, 1, 1) -> True (center)
        is_valid_cell_simple(board, -1, 0) -> False (out of bounds)
        is_valid_cell_simple(board, 3, 3) -> False (out of bounds)
    """
    try:
        height = len(board)
        width = len(board[0]) if height > 0 else 0
        return 0 <= row < height and 0 <= col < width
    except (TypeError, IndexError):
        return False


# Cached version that converts board to a hashable tuple
def is_valid_cell(board, row, col):
    """
    Checks if the cell coordinates are within the board boundaries.
    This version converts the board to a hashable type (tuple) for caching.
    
    Args:
        board: The game board as a 2D list
        row: Row index to check
        col: Column index to check
        
    Returns:
        True if the coordinates are valid, False otherwise
    """
    # Convert board to a hashable type (tuple of tuples)
    try:
        board_tuple = tuple(tuple(row) for row in board)
        return _is_valid_cell_cached(board_tuple, row, col)
    except (TypeError, IndexError):
        return False


@lru_cache(maxsize=128)
def _is_valid_cell_cached(board_tuple, row, col):
    """
    Cached version of is_valid_cell that works with hashable board representation.
    The @lru_cache decorator memoizes results for better performance.
    
    Args:
        board_tuple: The game board as a tuple of tuples (hashable)
        row: Row index to check
        col: Column index to check
        
    Returns:
        True if the coordinates are valid, False otherwise
    """
    try:
        height = len(board_tuple)
        width = len(board_tuple[0]) if height > 0 else 0
        return 0 <= row < height and 0 <= col < width
    except (TypeError, IndexError):
        return False


def get_game_from_board(board):
    """
    Retrieves the Game object associated with the given player board.
    This is used to find the game in the database when only the board is available.
    
    Args:
        board: The player's visible board
        
    Returns:
        Game object if found, None otherwise
    """
    return Game.objects.filter(player_board=board).first()


# Simple version without caching for direct use with lists
def count_adjacent_mines_simple(board, row, col):
    """
    Counts the number of mines adjacent to the given cell.
    This is a simple version that works directly with list boards.
    
    Args:
        board: The board containing mine positions (internal board)
        row: Row index of the cell
        col: Column index of the cell
        
    Returns:
        Number of adjacent mines (0-8)
        
    Example:
        For board = [['', 'M', ''], ['M', '', 'M'], ['', 'M', '']]
        count_adjacent_mines_simple(board, 1, 1) -> 4 (center cell has 4 adjacent mines)
        count_adjacent_mines_simple(board, 0, 0) -> 2 (top-left corner has 2 adjacent mines)
    """
    count = 0
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    
    # Check all 8 adjacent cells (horizontally, vertically, and diagonally)
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
    Counts the number of mines adjacent to the given cell.
    This version converts the board to a hashable type (tuple) for caching.
    
    Args:
        board: The board containing mine positions (internal board)
        row: Row index of the cell
        col: Column index of the cell
        
    Returns:
        Number of adjacent mines (0-8)
    """
    # Convert board to a hashable type (tuple of tuples)
    try:
        board_tuple = tuple(tuple(row) for row in board)
        return _count_adjacent_mines_cached(board_tuple, row, col)
    except (TypeError, IndexError):
        return 0


@lru_cache(maxsize=1024)
def _count_adjacent_mines_cached(board_tuple, row, col):
    """
    Cached version of count_adjacent_mines that works with hashable board representation.
    The @lru_cache decorator memoizes results for better performance.
    
    Args:
        board_tuple: The game board as a tuple of tuples (hashable)
        row: Row index of the cell
        col: Column index of the cell
        
    Returns:
        Number of adjacent mines (0-8)
    """
    count = 0
    height = len(board_tuple)
    width = len(board_tuple[0]) if height > 0 else 0
    
    # Check all 8 adjacent cells (horizontally, vertically, and diagonally)
    for i in range(max(0, row-1), min(height, row+2)):
        for j in range(max(0, col-1), min(width, col+2)):
            if i == row and j == col:
                continue  # Skip the cell itself
            if board_tuple[i][j] == 'M':
                count += 1
    return count