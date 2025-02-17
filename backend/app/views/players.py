# -*- coding: utf-8 -*-
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from app.dbmodels import Player, Game, Shot  # Import your relevant models

LOGGER = logging.getLogger('django')


class PlayerSummary(APIView):
    logger = LOGGER

    def get(self, request, playerID):
        """Return player data"""
        try:
            # Retrieve the player
            player = Player.objects.get(id=playerID)
            
            # Fetch games and shots related to the player
            games = Game.objects.filter(player=player)
            player_summary = {
                'name': player.name,
                'games': []
            }

            for game in games:
                shots = Shot.objects.filter(game=game)
                shots_data = []
                for shot in shots:
                    shots_data.append({
                        'made': shot.made,
                        'coordinates': (shot.x_coordinate, shot.y_coordinate),
                    })

                player_summary['games'].append({
                    'date': game.date,
                    'starter': game.starter,
                    'minutes': game.minutes,
                    'points': game.points,
                    'assists': game.assists,
                    'rebounds': game.rebounds,
                    'shots': shots_data
                })

            return Response(player_summary)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
