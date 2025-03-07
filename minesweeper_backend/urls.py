from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.create_game, name='create_game'),       # POST: Create a new game
    path('games/<uuid:game_id>/', views.get_game, name='get_game'),  # GET: Retrieve game state
    path('games/<uuid:game_id>/reveal/', views.reveal, name='reveal'),  # POST: Reveal a cell
]