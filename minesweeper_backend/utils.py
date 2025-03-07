import random

from minesweeper_backend.models import Game

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
    if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]) or board[row][col] != '':
        return 0  # Out of bounds, already revealed, or already flagged

    # Get the game object and its internal board with mines
    game = Game.objects.filter(player_board=board).first()
    if not game:
        return 0  # Game not found
    
    internal_board = game.internal_board
    
    # Check if the cell contains a mine
    if internal_board[row][col] == 'M':
        board[row][col] = 'M'  # Game Over - reveal the mine
        return -1  # Return -1 to indicate game over
    
    # Count adjacent mines
    mine_count = count_adjacent_mines(internal_board, row, col)
    board[row][col] = str(mine_count) if mine_count > 0 else '0'
    
    # If no adjacent mines, recursively reveal adjacent cells
    if mine_count == 0:
        # Reveal adjacent cells
        for i in range(max(0, row-1), min(len(board), row+2)):
            for j in range(max(0, col-1), min(len(board[0]), col+2)):
                if board[i][j] == '':  # If not already revealed
                    reveal_cell(board, i, j)
    
    return 1  # Cell revealed successfully

def count_adjacent_mines(board, row, col):
    count = 0
    for i in range(max(0, row-1), min(len(board), row+2)):
        for j in range(max(0, col-1), min(len(board[0]), col+2)):
            if i == row and j == col:
                continue  # Skip the cell itself
            if board[i][j] == 'M':
                count += 1
    return count