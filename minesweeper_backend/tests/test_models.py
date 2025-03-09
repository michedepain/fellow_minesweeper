from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import patch

from minesweeper_backend.models import Game


class GameModelTest(TestCase):
    """Test cases for the Game model"""

    def setUp(self):
        """Set up test data"""
        self.valid_game_data = {
            'width': 10,
            'height': 10,
            'mines': 10
        }

    def test_game_creation(self):
        """Test that a game can be created with valid parameters"""
        game = Game.objects.create(**self.valid_game_data)
        self.assertIsNotNone(game.id)
        self.assertEqual(game.width, 10)
        self.assertEqual(game.height, 10)
        self.assertEqual(game.mines, 10)
        self.assertIsNone(game.internal_board)
        self.assertIsNone(game.player_board)
        self.assertEqual(game.revealed_cells, 0)
        self.assertFalse(game.game_over)
        self.assertFalse(game.game_won)
        self.assertIsNotNone(game.created_at)

    def test_clean_valid_mines(self):
        """Test that clean passes with valid number of mines"""
        game = Game(**self.valid_game_data)
        # This should not raise an exception
        game.clean()

    def test_clean_mines_validation(self):
        """Test that clean raises ValidationError with too many mines"""
        game = Game(width=5, height=5, mines=24)
        game.clean()

        game = Game(width=5, height=5, mines=25)
        with self.assertRaises(ValidationError):
            game.clean()

        game = Game(width=5, height=5, mines=26)
        with self.assertRaises(ValidationError):
            game.clean()

    @patch('minesweeper_backend.utils.generate_minesweeper_board')
    def test_initialize_board(self, mock_generate_board):
        """Test that initialize_board correctly sets up the game boards"""
        mock_generate_board.return_value = {
            'internal_board': [['', 'M', ''], ['', '', 'M']],
            'player_board': [['', '', ''], ['', '', '']]
        }

        game = Game.objects.create(**self.valid_game_data)
        game.initialize_board()

        self.assertEqual(game.internal_board, [['', 'M', ''], ['', '', 'M']])
        self.assertEqual(game.player_board, [['', '', ''], ['', '', '']])

        mock_generate_board.assert_called_once_with(10, 10, 10)

    def test_initialize_board_already_initialized(self):
        """Test that initialize_board raises ValidationError if boards already exist"""
        game = Game.objects.create(
            width=5,
            height=5,
            mines=5,
            internal_board=[['', 'M', ''], ['', '', 'M']],
            player_board=[['', '', ''], ['', '', '']]
        )

        with self.assertRaises(ValidationError):
            game.initialize_board()

    def test_board_dimensions(self):
        """Test that the board dimensions match the width and height"""
        game = Game.objects.create(width=3, height=4, mines=2)
        
        # Mock the board generation to return predictable results
        with patch('minesweeper_backend.utils.generate_minesweeper_board') as mock_generate:
            internal_board = [['', '', ''] for _ in range(4)]
            player_board = [['', '', ''] for _ in range(4)]
            
            mock_generate.return_value = {
                'internal_board': internal_board,
                'player_board': player_board
            }
            
            game.initialize_board()
            
            self.assertEqual(len(game.internal_board), 4)
            self.assertEqual(len(game.internal_board[0]), 3)
            self.assertEqual(len(game.player_board), 4)
            self.assertEqual(len(game.player_board[0]), 3)

    def test_mine_count(self):
        """Test that the internal board has the correct number of mines"""
        game = Game.objects.create(width=5, height=5, mines=7)
        
        game.initialize_board()
        
        mine_count = sum(row.count('M') for row in game.internal_board)
        
        self.assertEqual(mine_count, 7)

    def test_player_board_initially_empty(self):
        """Test that the player board is initially all empty"""
        game = Game.objects.create(width=5, height=5, mines=5)
        game.initialize_board()
        
        for row in game.player_board:
            for cell in row:
                self.assertEqual(cell, '') 