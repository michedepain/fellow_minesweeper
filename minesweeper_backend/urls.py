from django.urls import path
from . import views

urlpatterns = [
    path('games/', views.create_game, name='create_game'),
    path('games/<uuid:game_id>/', views.get_game, name='get_game'),
    path('games/<uuid:game_id>/reveal/', views.reveal, name='reveal'),
]