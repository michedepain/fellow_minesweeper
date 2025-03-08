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
        
        self.assertEqual(len(boards['internal_board']), height)
        self.assertEqual(len(boards['internal_board'][0]), width)
        
        self.assertEqual(len(boards['player_board']), height)
        self.assertEqual(len(boards['player_board'][0]), width)

    def test_mine_count(self):
        """Test that the correct number of mines are placed"""
        width, height, mines = 10, 10, 15
        boards = generate_minesweeper_board(width, height, mines)
        
        mine_count = sum(row.count('M') for row in boards['internal_board'])
        self.assertEqual(mine_count, mines)

    def test_player_board_empty(self):
        """Test that the player board is initially empty"""
        width, height, mines = 5, 5, 5
        boards = generate_minesweeper_board(width, height, mines)
        
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
        self.assertEqual(count, 4)

    def test_corner_cell(self):
        """Test counting mines around a corner cell"""
        count = count_adjacent_mines(self.board, 0, 0)
        self.assertEqual(count, 2)

    def test_edge_cell(self):
        """Test counting mines around an edge cell"""
        count = count_adjacent_mines(self.board, 0, 1)
        self.assertEqual(count, 2)

    def test_mine_cell(self):
        """Test counting mines around a cell that is itself a mine"""
        count = count_adjacent_mines(self.board, 1, 0)
        self.assertEqual(count, 2)


class RevealCellTest(TestCase):
    """Test cases for the reveal_cell function"""

    def setUp(self):
        """Set up test game and boards"""
        self.game = Game.objects.create(
            width=3,
            height=3,
            mines=4
        )
        
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
        result = reveal_cell(self.game.player_board, 0, 0)
        
        self.assertEqual(result, -1)
        
        self.assertEqual(self.game.player_board[0][0], 'M')

    def test_reveal_cell_with_adjacent_mines(self):
        """Test revealing a cell with adjacent mines"""
        result = reveal_cell(self.game.player_board, 1, 1)
        
        self.assertEqual(result, 1)
        
        self.assertEqual(self.game.player_board[1][1], '4')

    def test_recursive_reveal(self):
        """Test recursive revealing of cells with no adjacent mines"""
        game = Game.objects.create(
            width=3,
            height=3,
            mines=1
        )
        
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
        
        game.internal_board = internal_board
        game.player_board = player_board
        game.save()
        
        with patch('minesweeper_backend.utils.get_game_from_board') as mock_get_game:
            mock_get_game.return_value = game
            
            result = reveal_cell(player_board, 0, 0)
            
            self.assertEqual(result, 1)
            
            self.assertEqual(player_board[0][0], '0')
            
            revealed_count = sum(1 for row in player_board for cell in row if cell != '')
            self.assertEqual(revealed_count, 8)

    def test_reveal_already_revealed_cell(self):
        """Test revealing an already revealed cell"""
        reveal_cell(self.game.player_board, 1, 1)
        
        result = reveal_cell(self.game.player_board, 1, 1)
        
        self.assertEqual(result, 0)

    def test_reveal_out_of_bounds(self):
        """Test revealing a cell outside the board boundaries"""
        result = reveal_cell(self.game.player_board, -1, 0)
        
        self.assertEqual(result, 0)
        
        result = reveal_cell(self.game.player_board, 0, 3)
        self.assertEqual(result, 0)

    @patch('minesweeper_backend.models.Game.objects.filter')
    def test_game_not_found(self, mock_filter):
        """Test revealing a cell when the game is not found"""
        mock_filter.return_value.first.return_value = None
        
        board = [['', '', ''], ['', '', ''], ['', '', '']]
        
        result = reveal_cell(board, 0, 0)
        self.assertEqual(result, 0)
        
        mock_filter.assert_called_once() 