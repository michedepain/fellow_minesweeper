from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import uuid
from unittest.mock import patch, MagicMock

from minesweeper_backend.models import Game


class CreateGameViewTest(TestCase):
    """Test cases for the create_game view"""

    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
        self.url = reverse('create_game')

    def test_create_game_success(self):
        """Test successful game creation"""
        data = {
            'width': 10,
            'height': 10,
            'mines': 10
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('game_id', response.data)
        self.assertEqual(response.data['width'], 10)
        self.assertEqual(response.data['height'], 10)
        self.assertEqual(response.data['mines'], 10)
        self.assertIn('board_state', response.data)
        
        game_id = response.data['game_id']
        game = Game.objects.get(id=game_id)
        self.assertEqual(game.width, 10)
        self.assertEqual(game.height, 10)
        self.assertEqual(game.mines, 10)
        self.assertIsNotNone(game.internal_board)
        self.assertIsNotNone(game.player_board)

    def test_create_game_default_values(self):
        """Test game creation with default values"""
        response = self.client.post(self.url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['width'], 10)  # Default width
        self.assertEqual(response.data['height'], 10)  # Default height
        self.assertEqual(response.data['mines'], 10)  # Default mines

    def test_create_game_invalid_dimensions(self):
        """Test game creation with invalid dimensions"""
        data = {'width': -5, 'height': 10, 'mines': 10}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {'width': 10, 'height': 0, 'mines': 10}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_too_many_mines(self):
        """Test game creation with too many mines"""
        data = {'width': 5, 'height': 5, 'mines': 25}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_game_non_integer_values(self):
        """Test game creation with non-integer values"""
        data = {'width': 'abc', 'height': 10, 'mines': 10}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetGameViewTest(TestCase):
    """Test cases for the get_game view"""

    def setUp(self):
        """Set up test client and create a test game"""
        self.client = APIClient()
        self.game = Game.objects.create(width=8, height=8, mines=8)
        self.game.initialize_board()
        self.url = reverse('get_game', args=[self.game.id])

    def test_get_game_success(self):
        """Test successful game retrieval"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['game_id']), str(self.game.id))
        self.assertEqual(response.data['width'], 8)
        self.assertEqual(response.data['height'], 8)
        self.assertEqual(response.data['mines'], 8)
        self.assertEqual(response.data['board_state'], self.game.player_board)
        self.assertEqual(response.data['game_over'], False)
        self.assertEqual(response.data['game_won'], False)

    def test_get_game_not_found(self):
        """Test game retrieval with non-existent ID"""
        non_existent_id = uuid.uuid4()
        url = reverse('get_game', args=[non_existent_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RevealViewTest(TestCase):
    """Test cases for the reveal view"""

    def setUp(self):
        """Set up test client and create a test game"""
        self.client = APIClient()
        self.game = Game.objects.create(width=5, height=5, mines=5)
        self.game.initialize_board()
        self.url = reverse('reveal', args=[self.game.id])

    def test_reveal_cell_success(self):
        """Test successful cell reveal"""
        row, col = self._find_safe_cell()
        
        data = {'row': row, 'col': col}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Cell revealed")
        self.assertEqual(str(response.data['game_id']), str(self.game.id))
        
        self.game.refresh_from_db()
        self.assertNotEqual(self.game.player_board[row][col], '')

    def test_reveal_mine_cell(self):
        """Test revealing a cell with a mine"""
        row, col = self._find_mine_cell()
        
        data = {'row': row, 'col': col}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Game Over! You hit a mine!")
        
        self.game.refresh_from_db()
        self.assertEqual(self.game.player_board[row][col], 'M')
        self.assertTrue(self.game.game_over)

    def test_reveal_already_revealed_cell(self):
        """Test revealing an already revealed cell"""
        row, col = self._find_safe_cell()
        
        data = {'row': row, 'col': col}
        self.client.post(self.url, data, format='json')
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Cell already revealed")

    def test_reveal_out_of_bounds(self):
        """Test revealing a cell outside the board boundaries"""
        data = {'row': -1, 'col': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {'row': 0, 'col': self.game.width}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reveal_missing_parameters(self):
        """Test revealing without providing row or column"""
        data = {'row': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {'col': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reveal_non_integer_parameters(self):
        """Test revealing with non-integer row or column"""
        data = {'row': 'abc', 'col': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reveal_game_already_over(self):
        """Test revealing when game is already over"""
        self.game.game_over = True
        self.game.save()
        
        data = {'row': 0, 'col': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_reveal_game_already_won(self):
        """Test revealing when game is already won"""
        self.game.game_won = True
        self.game.save()
        
        data = {'row': 0, 'col': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('minesweeper_backend.utils.reveal_cell')
    def test_win_condition(self, mock_reveal_cell):
        """Test that game is marked as won when all non-mine cells are revealed"""
        mock_reveal_cell.return_value = 1
        
        game = Game.objects.create(width=5, height=5, mines=5)
        game.initialize_board()
        game.revealed_cells = 19  # One cell away from winning
        game.save()
        
        url = reverse('reveal', args=[game.id])
        data = {'row': 0, 'col': 0}
        response = self.client.post(url, data, format='json')
        
        game.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(game.game_won)

    def _find_safe_cell(self):
        """Helper method to find a cell without a mine"""
        for row in range(self.game.height):
            for col in range(self.game.width):
                if self.game.internal_board[row][col] != 'M':
                    return row, col
        return 0, 0

    def _find_mine_cell(self):
        """Helper method to find a cell with a mine"""
        for row in range(self.game.height):
            for col in range(self.game.width):
                if self.game.internal_board[row][col] == 'M':
                    return row, col
        return 0, 0 