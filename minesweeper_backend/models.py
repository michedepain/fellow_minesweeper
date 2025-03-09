from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.cache import cache

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    width = models.IntegerField()
    height = models.IntegerField()
    mines = models.IntegerField()
    internal_board = models.JSONField(
        null=True,
        blank=True
    )  # [['', 'M', ''], ['', 'M', ''], ...] - Contains the actual mine positions
    player_board = models.JSONField(
        null=True,
        blank=True
    )  # [['', '', ''], ['', '', ''], ...] - What the player sees, initially all hidden
    revealed_cells = models.IntegerField(default=0)
    game_over = models.BooleanField(default=False)
    game_won = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
         if self.mines >= self.width * self.height:
             raise ValidationError("Too many mines for the given board size.")

    def initialize_board(self):
        from .utils import generate_minesweeper_board
        if self.internal_board is not None or self.player_board is not None:
            raise ValidationError("Board already initialized")
        
        boards = generate_minesweeper_board(self.width, self.height, self.mines)
        self.internal_board = boards['internal_board']
        self.player_board = boards['player_board']
        self.save()
    
    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)
        
        # Invalidate cache for this game
        self.invalidate_cache()
    
    def invalidate_cache(self):
        """Invalidate the cache for this game."""
        cache_key = f"game_{self.id}"
        cache.delete(cache_key)
    
    def __str__(self):
        return f"Game {self.id} - {self.width}x{self.height} with {self.mines} mines"
