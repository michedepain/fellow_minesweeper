from django.forms import ValidationError

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Game
from .utils import reveal_cell
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import time
import logging
from django.http import Http404

logger = logging.getLogger(__name__)

def get_game_cache_key(game_id):
    return f"game_{game_id}"

@api_view(['POST'])
@permission_classes([AllowAny])
def create_game(request):
     start_time = time.time()
     
     try:
         width_param = request.data.get('width', 10)
         height_param = request.data.get('height', 10)
         mines_param = request.data.get('mines', 10)
         
         try:
             width = int(width_param)
             height = int(height_param)
             mines = int(mines_param)
         except ValueError:
             return Response({"error": "Width, height, and mines must be integers."}, status=status.HTTP_400_BAD_REQUEST)

         if not all([width, height, mines]):
             return Response({"error": "Width, height, and mines are required."}, status=status.HTTP_400_BAD_REQUEST)
         if width <= 0 or height <= 0:
             return Response({"error": "Width and height should be > 0."}, status=status.HTTP_400_BAD_REQUEST)

         try:
             game = Game(width=width, height=height, mines=mines)
             game.full_clean()
             game.initialize_board()
             game.save()
             
             # Cache the new game
             cache_key = get_game_cache_key(game.id)
             game_data = {
                 'game_id': game.id,
                 'width': game.width,
                 'height': game.height,
                 'mines': game.mines,
                 'board_state': game.player_board,
                 'game_over': game.game_over,
                 'game_won': game.game_won
             }
             cache.set(cache_key, game_data, timeout=3600)  # Cache for 1 hour
             
         except ValidationError as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

         elapsed_time = time.time() - start_time
         logger.info(f"Created game {game.id} in {elapsed_time:.4f} seconds")
         
         return Response(game_data, status=status.HTTP_201_CREATED)
     
     except Exception as e:
         logger.error(f"Error in create_game view: {str(e)}", exc_info=True)
         return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def reveal(request, game_id):
     start_time = time.time()
     cache_hit = False
     
     try:
         cache_key = get_game_cache_key(game_id)
         cached_game_data = cache.get(cache_key)
         
         if not cached_game_data:
             logger.debug(f"Cache miss for game {game_id}")
             game = get_object_or_404(Game, pk=game_id)
         else:
             logger.debug(f"Cache hit for game {game_id}")
             cache_hit = True

             game = get_object_or_404(Game, pk=game_id)

         if game.game_over or game.game_won:
             elapsed_time = time.time() - start_time
             logger.info(f"Rejected reveal for finished game {game_id} in {elapsed_time:.4f} seconds")
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
             # Return cached data if available
             game_data = {
                 'message': "Cell already revealed", 
                 'game_id': game.id,
                 'board_state': game.player_board, 
                 'game_over': game.game_over, 
                 'game_won': game.game_won
             }
             elapsed_time = time.time() - start_time
             logger.info(f"Cell already revealed for game {game_id} (cache hit: {cache_hit}) in {elapsed_time:.4f} seconds")
             return Response(game_data, status=status.HTTP_200_OK)

         reveal_start_time = time.time()
         with transaction.atomic(): 
             game = Game.objects.select_for_update().get(pk=game_id) 

             revealed_count = reveal_cell(game.player_board, row, col, internal_board=game.internal_board, game=game)
             reveal_elapsed = time.time() - reveal_start_time
             logger.debug(f"Revealed {revealed_count} cells in {reveal_elapsed:.4f} seconds")

             if revealed_count == -1:
                 game.game_over = True
                 game.save()
                 
                 # Update cache
                 game_data = {
                     'message': "Game Over! You hit a mine!", 
                     'game_id': game.id,
                     'board_state': game.player_board, 
                     'game_over': game.game_over, 
                     'game_won': game.game_won 
                 }
                 cache.set(cache_key, game_data, timeout=3600) 
                 
                 elapsed_time = time.time() - start_time
                 logger.info(f"Game over for game {game_id} in {elapsed_time:.4f} seconds")
                 return Response(game_data, status=status.HTTP_200_OK)

             if isinstance(revealed_count, int) and revealed_count > 0:
                 game.revealed_cells += revealed_count
             
             if game.revealed_cells >= game.width * game.height - game.mines:
                 game.game_won = True
                 logger.info(f"Game {game_id} won!")

             game.save()
             
             game_data = {
                 'message': "Cell revealed", 
                 'game_id': game.id,
                 'board_state': game.player_board, 
                 'game_over': game.game_over, 
                 'game_won': game.game_won,
                 'revealed_count': revealed_count
             }
             cache.set(cache_key, game_data, timeout=3600)
         
         elapsed_time = time.time() - start_time
         logger.info(f"Revealed cell ({row}, {col}) for game {game_id} in {elapsed_time:.4f} seconds, revealed {revealed_count} cells")
         return Response(game_data, status=status.HTTP_200_OK)
     
     except Exception as e:
         logger.error(f"Error in reveal view: {str(e)}", exc_info=True)
         return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 5)
def get_game(request, game_id):
     start_time = time.time()
     
     try:
         cache_key = get_game_cache_key(game_id)
         cached_game_data = cache.get(cache_key)
         
         if cached_game_data:
             logger.debug(f"Cache hit for game {game_id}")
             elapsed_time = time.time() - start_time
             logger.info(f"Retrieved game {game_id} from cache in {elapsed_time:.4f} seconds")
             return Response(cached_game_data, status=status.HTTP_200_OK)
         
         logger.debug(f"Cache miss for game {game_id}")
         
         try:
             game = get_object_or_404(Game, pk=game_id)
         except Http404:
             logger.info(f"Game {game_id} not found")
             return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
         
         game_data = {
             'game_id': game.id,
             'width': game.width,
             'height': game.height,
             'mines': game.mines,
             'board_state': game.player_board,
             'game_over': game.game_over,
             'game_won': game.game_won
         }
         
         cache.set(cache_key, game_data, timeout=3600)
         
         elapsed_time = time.time() - start_time
         logger.info(f"Retrieved game {game_id} from database in {elapsed_time:.4f} seconds")
         return Response(game_data, status=status.HTTP_200_OK)
     
     except Exception as e:
         logger.error(f"Error in get_game view: {str(e)}", exc_info=True)
         if isinstance(e, Http404):
             return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
         return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
