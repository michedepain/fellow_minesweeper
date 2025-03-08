from django.test import TestCase
from unittest.mock import patch, MagicMock, call

from minesweeper_backend.utils import generate_minesweeper_board, reveal_cell, count_adjacent_mines
from minesweeper_backend.models import Game


class GenerateMinesweeperBoardTest(TestCase):
    """Test cases for the generate_minesweeper_board function"""

    def test_board_dimensions(self):
        """Test that the generated boards have the correct dimensions"""
        width, height, mines = 8, 6, 10
        boards = generate_minesweeper_board(width, height, mines)
        
        # Check internal board dimensions
        self.assertEqual(len(boards['internal_board']), height)
        self.assertEqual(len(boards['internal_board'][0]), width)
        
        # Check player board dimensions
        self.assertEqual(len(boards['player_board']), height)
        self.assertEqual(len(boards['player_board'][0]), width)

    def test_mine_count(self):
        """Test that the correct number of mines are placed"""
        width, height, mines = 10, 10, 15
        boards = generate_minesweeper_board(width, height, mines)
        
        # Count mines in the internal board
        mine_count = sum(row.count('M') for row in boards['internal_board'])
        self.assertEqual(mine_count, mines)

    def test_player_board_empty(self):
        """Test that the player board is initially empty"""
        width, height, mines = 5, 5, 5
        boards = generate_minesweeper_board(width, height, mines)
        
        # Check that all cells in player board are empty
        for row in boards['player_board']:
            for cell in row:
                self.assertEqual(cell, '')


class CountAdjacentMinesTest(TestCase):
    """Test cases for the count_adjacent_mines function"""

    def setUp(self):
        """Set up test board"""
        self.board = [
            ['', 'M', ''],
            ['M', '', 'M'],
            ['', 'M', '']
        ]

    def test_center_cell(self):
        """Test counting mines around the center cell"""
        count = count_adjacent_mines(self.board, 1, 1)
        self.assertEqual(count, 4)  # Should have 4 adjacent mines

    def test_corner_cell(self):
        """Test counting mines around a corner cell"""
        count = count_adjacent_mines(self.board, 0, 0)
        self.assertEqual(count, 2)  # Should have 2 adjacent mines

    def test_edge_cell(self):
        """Test counting mines around an edge cell"""
        count = count_adjacent_mines(self.board, 0, 1)
        self.assertEqual(count, 2)  # Should have 2 adjacent mines

    def test_mine_cell(self):
        """Test counting mines around a cell that is itself a mine"""
        count = count_adjacent_mines(self.board, 1, 0)
        self.assertEqual(count, 2)  # Should have 2 adjacent mines


class RevealCellTest(TestCase):
    """Test cases for the reveal_cell function"""

    def setUp(self):
        """Set up test game and boards"""
        self.game = Game.objects.create(
            width=3,
            height=3,
            mines=4
        )
        
        # Create a known board layout for testing
        self.internal_board = [
            ['M', '', 'M'],
            ['', '', ''],
            ['M', '', 'M']
        ]
        
        self.player_board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        
        self.game.internal_board = self.internal_board
        self.game.player_board = self.player_board
        self.game.save()

    def test_reveal_mine(self):
        """Test revealing a cell with a mine"""
        # Reveal a cell with a mine (0, 0)
        result = reveal_cell(self.game.player_board, 0, 0)
        
        # Should return -1 to indicate game over
        self.assertEqual(result, -1)
        
        # The mine should be revealed in the player board
        self.assertEqual(self.game.player_board[0][0], 'M')

    def test_reveal_cell_with_adjacent_mines(self):
        """Test revealing a cell with adjacent mines"""
        # Reveal center cell (1, 1) which has 4 adjacent mines
        result = reveal_cell(self.game.player_board, 1, 1)
        
        # Should return 1 to indicate one cell revealed
        self.assertEqual(result, 1)
        
        # The cell should show the number of adjacent mines
        self.assertEqual(self.game.player_board[1][1], '4')

    def test_recursive_reveal(self):
        """Test recursive revealing of cells with no adjacent mines"""
        # Create a new test game with a simple board
        game = Game.objects.create(
            width=3,
            height=3,
            mines=1
        )
        
        # Set up a board with a single mine in the bottom-right corner
        internal_board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', 'M']
        ]
        
        player_board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        
        # Manually set the boards
        game.internal_board = internal_board
        game.player_board = player_board
        game.save()
        
        # Create a mock for the get_game_from_board function to return our game
        with patch('minesweeper_backend.utils.get_game_from_board') as mock_get_game:
            mock_get_game.return_value = game
            
            # Reveal the top-left cell (0, 0)
            result = reveal_cell(player_board, 0, 0)
            
            # Should return 1 for successful reveal
            self.assertEqual(result, 1)
            
            # The cell should show '0' for no adjacent mines
            self.assertEqual(player_board[0][0], '0')
            
            # Multiple cells should be revealed due to recursion
            revealed_count = sum(1 for row in player_board for cell in row if cell != '')
            self.assertEqual(revealed_count, 8)

    def test_reveal_already_revealed_cell(self):
        """Test revealing an already revealed cell"""
        # First reveal a cell
        reveal_cell(self.game.player_board, 1, 1)
        
        # Try to reveal the same cell again
        result = reveal_cell(self.game.player_board, 1, 1)
        
        # Should return 0 to indicate no new cells revealed
        self.assertEqual(result, 0)

    def test_reveal_out_of_bounds(self):
        """Test revealing a cell outside the board boundaries"""
        # Try to reveal a cell outside the board
        result = reveal_cell(self.game.player_board, -1, 0)
        
        # Should return 0 to indicate no cells revealed
        self.assertEqual(result, 0)
        
        result = reveal_cell(self.game.player_board, 0, 3)
        self.assertEqual(result, 0)

    @patch('minesweeper_backend.models.Game.objects.filter')
    def test_game_not_found(self, mock_filter):
        """Test revealing a cell when the game is not found"""
        # Mock the filter method to return an empty queryset
        mock_filter.return_value.first.return_value = None
        
        # Create a board not associated with any game
        board = [['', '', ''], ['', '', ''], ['', '', '']]
        
        # Should return 0 to indicate no cells revealed
        result = reveal_cell(board, 0, 0)
        self.assertEqual(result, 0)
        
        # Verify the filter method was called with the correct arguments
        mock_filter.assert_called_once() 