from django.forms import ValidationError
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Game
from .utils import reveal_cell, generate_minesweeper_board
from django.db import transaction

@api_view(['POST'])
@permission_classes([AllowAny])  #  Anyone can create a new game
def create_game(request):
     # Get parameters with default values
     width_param = request.data.get('width', 10)
     height_param = request.data.get('height', 10)
     mines_param = request.data.get('mines', 10)
     
     # Convert to integers
     try:
         width = int(width_param)
         height = int(height_param)
         mines = int(mines_param)
     except ValueError:
         return Response({"error": "Width, height, and mines must be integers."}, status=status.HTTP_400_BAD_REQUEST)

     # Validate parameters
     if not all([width, height, mines]):
         return Response({"error": "Width, height, and mines are required."}, status=status.HTTP_400_BAD_REQUEST)
     if width <= 0 or height <= 0:
         return Response({"error": "Width and height should be > 0."}, status=status.HTTP_400_BAD_REQUEST)

     # Create and initialize game
     try:
         game = Game(width=width, height=height, mines=mines)
         game.full_clean()  # Run model validations
         game.initialize_board() # Initialize and save
         game.save()
     except ValidationError as e:
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

     # Return success response
     return Response({
         'game_id': game.id,
         'width': game.width,
         'height': game.height,
         'mines': game.mines,
         'board_state': game.player_board  # Send only the player's view board
     }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])  # Keep it simple for now
def reveal(request, game_id):
     game = get_object_or_404(Game, pk=game_id)

     if game.game_over or game.game_won:
         return Response({"error": "Game already finished."}, status=status.HTTP_400_BAD_REQUEST)

     row = request.data.get('row')
     col = request.data.get('col')

     if row is None or col is None:
         return Response({"error": "Row and column are required."}, status=status.HTTP_400_BAD_REQUEST)

     try:
         row = int(row)
         col = int(col)
     except ValueError:
         return Response({"error": "Invalid row or column values."}, status=status.HTTP_400_BAD_REQUEST)

     if row < 0 or row >= game.height or col < 0 or col >= game.width:
          return Response({"error": "Out of bounds"}, status=status.HTTP_400_BAD_REQUEST)

     if game.player_board[row][col] != '':
         return Response({
             'message': "Cell already revealed", 
             'game_id': game.id,  # Include game_id in the response
             'board_state': game.player_board, 
             'game_over': game.game_over, 
             'game_won': game.game_won
         }, status=status.HTTP_200_OK)

     with transaction.atomic(): 
         game = Game.objects.select_for_update().get(pk=game_id) 

         revealed_count = reveal_cell(game.player_board, row, col)

         if revealed_count == -1:
             game.game_over = True #Set game over
             game.save()
             return Response({
                 'message': "Game Over! You hit a mine!", 
                 'game_id': game.id,  # Include game_id in the response
                 'board_state': game.player_board, 
                 'game_over': game.game_over, 
                 'game_won': game.game_won 
             }, status=status.HTTP_200_OK)

         game.revealed_cells += revealed_count
         if game.revealed_cells == game.width * game.height - game.mines:
             game.game_won = True

         game.save()

     return Response({
         'message': "Cell revealed", 
         'game_id': game.id,  # Include game_id in the response
         'board_state': game.player_board, 
         'game_over': game.game_over, 
         'game_won': game.game_won
     }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])  # Anyone can retrieve the game state.
def get_game(request, game_id):
     game = get_object_or_404(Game, pk=game_id)
     return Response({
         'game_id': game.id,
         'width': game.width,
         'height': game.height,
         'mines': game.mines,
         'board_state': game.player_board,  # Send only the player's view board
         'game_over': game.game_over,
         'game_won': game.game_won
     }, status=status.HTTP_200_OK)
