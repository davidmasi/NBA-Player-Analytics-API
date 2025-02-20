import json
import os
from django.db import transaction
from django.core.management.base import BaseCommand
from app.models import Team, Player, Game, GamePlayerStats, Shot

class Command(BaseCommand):
    help = 'Load game data from JSON files'

    def handle(self, *args, **kwargs):
        try:
            self._load_data()
            self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {str(e)}'))

    def _load_json_file(self, filename):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        file_path = os.path.join(base_dir, 'raw_data', filename)
        with open(file_path, 'r') as file:
            return json.load(file)
    # @transaction.atomic decorator ensures that all database operations within _load_data()
    # are treated as a single transaction. If any error occurs, the entire transaction is 
    # rolled back, preventing partial data loads. This is crucial for data integrity.
    @transaction.atomic
    def _load_data(self):
        # Load teams
        teams_data = self._load_json_file('teams.json')
        team_objects = []
        for team in teams_data:
            team_obj, _ = Team.objects.update_or_create(
                id=team['id'],
                defaults={'name': team['name']}
            )
            team_objects.append(team_obj)

        # Load players
        players_data = self._load_json_file('players.json')
        player_objects = []
        for player in players_data:
            player_obj, _ = Player.objects.update_or_create(
                id=player['id'],
                defaults={'name': player['name']}
            )
            player_objects.append(player_obj)

        # Load games
        games_data = self._load_json_file('games.json')
        for game_data in games_data:
            # Create or update game
            game, _ = Game.objects.update_or_create(
                id=game_data['id'],
                defaults={
                    'date': game_data['date'],
                    'home_team_id': game_data['homeTeam']['id'],
                    'away_team_id': game_data['awayTeam']['id']
                }
            )

            # Process player stats for both teams
            for team_type in ['homeTeam', 'awayTeam']:
                team_data = game_data[team_type]
                team_id = team_data['id']

                for player_stats in team_data['players']:
                    # Create or update player game stats
                    game_player_stats, _ = GamePlayerStats.objects.update_or_create(
                        game=game,
                        player_id=player_stats['id'],
                        defaults={
                            'is_starter': player_stats['isStarter'],
                            'minutes': player_stats['minutes'],
                            'points': player_stats['points'],
                            'assists': player_stats['assists'],
                            'offensive_rebounds': player_stats['offensiveRebounds'],
                            'defensive_rebounds': player_stats['defensiveRebounds'],
                            'steals': player_stats['steals'],
                            'blocks': player_stats['blocks'],
                            'turnovers': player_stats['turnovers'],
                            'defensive_fouls': player_stats['defensiveFouls'],
                            'offensive_fouls': player_stats['offensiveFouls'],
                            'free_throws_made': player_stats['freeThrowsMade'],
                            'free_throws_attempted': player_stats['freeThrowsAttempted'],
                            'two_pointers_made': player_stats['twoPointersMade'],
                            'two_pointers_attempted': player_stats['twoPointersAttempted'],
                            'three_pointers_made': player_stats['threePointersMade'],
                            'three_pointers_attempted': player_stats['threePointersAttempted'],
                        }
                    )

                    # Delete existing shots for this game_player_stats and create new ones
                    Shot.objects.filter(game_player_stats=game_player_stats).delete()
                    shots = [
                        Shot(
                            game_player_stats=game_player_stats,
                            is_make=shot['isMake'],
                            location_x=shot['locationX'],
                            location_y=shot['locationY']
                        )
                        for shot in player_stats['shots']
                    ]
                    Shot.objects.bulk_create(shots)

                    # Update player's team
                    Player.objects.filter(id=player_stats['id']).update(team_id=team_id)
