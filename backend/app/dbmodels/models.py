# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models

class Team(models.Model):
    id = models.IntegerField(primary_key=True) # Use the ID from the JSON
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "teams"
    
    def __str__(self):
        return self.name

class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)  # No need for separate first/last name yet
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='roster')

    class Meta:
        db_table = "players"

    def __str__(self):
        return self.name
    
class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')

    class Meta:
        db_table = "games"
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"
    
class GamePlayerStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_game_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_game_stats')
    is_starter = models.BooleanField()
    minutes = models.IntegerField()
    points = models.IntegerField()
    assists = models.IntegerField()
    offensive_rebounds = models.IntegerField()
    defensive_rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    defensive_fouls = models.IntegerField()
    offensive_fouls = models.IntegerField()
    free_throws_made = models.IntegerField()
    free_throws_attempted = models.IntegerField()
    two_pointers_made = models.IntegerField()
    two_pointers_attempted = models.IntegerField()
    three_pointers_made = models.IntegerField()
    three_pointers_attempted = models.IntegerField()
    
    class Meta:
        db_table = "player_stats"
    
    def __str__(self):
        return f"{self.player} in {self.game}"
    
class Shot(models.Model):
    id = models.BigAutoField(primary_key=True)
    game_player_stats = models.ForeignKey(GamePlayerStats, on_delete=models.CASCADE, related_name='player_shots')
    is_make = models.BooleanField()
    location_x = models.DecimalField(max_digits=5, decimal_places=2)
    location_y = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "shots"

    def __str__(self):
        return f"Shot by {self.game_player_stats.player} in {self.game_player_stats.game}"