# -*- coding: utf-8 -*-
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from app.dbmodels.models import Player, GamePlayerStats
from django.db.models import Q

LOGGER = logging.getLogger('django')

class PlayerSearch(APIView):
    logger = LOGGER

    def get(self, request):
        """Search for players by name"""
        try:
            query = request.GET.get('query', '')
            if query:
                players = Player.objects.filter(
                    Q(name__icontains=query)
                ).values('id', 'name')[:10]
                return Response(list(players))
            return Response([])
        except Exception as e:
            self.logger.error(f"Error in player search: {str(e)}")
            return Response({'error': 'Search failed'}, status=500)

class PlayerSummary(APIView):
    logger = LOGGER

    def get(self, request, playerID):
        """Return player data"""
        try:
            player = Player.objects.get(id=playerID)
            game_stats = GamePlayerStats.objects.filter(player=player)
            
            player_summary = {
                'name': player.name,
                'games': []
            }

            for stats in game_stats:
                shots = stats.player_shots.all()
                shots_data = [
                    {
                        'isMake': shot.is_make,
                        'locationX': float(shot.location_x),
                        'locationY': float(shot.location_y)
                    } for shot in shots
                ]

                game_data = {
                    'date': stats.game.date.strftime('%Y-%m-%d'),
                    'isStarter': stats.is_starter,
                    'minutes': stats.minutes,
                    'points': stats.points,
                    'assists': stats.assists,
                    'offensiveRebounds': stats.offensive_rebounds,
                    'defensiveRebounds': stats.defensive_rebounds,
                    'steals': stats.steals,
                    'blocks': stats.blocks,
                    'turnovers': stats.turnovers,
                    'defensiveFouls': stats.defensive_fouls,
                    'offensiveFouls': stats.offensive_fouls,
                    'freeThrowsMade': stats.free_throws_made,
                    'freeThrowsAttempted': stats.free_throws_attempted,
                    'twoPointersMade': stats.two_pointers_made,
                    'twoPointersAttempted': stats.two_pointers_attempted,
                    'threePointersMade': stats.three_pointers_made,
                    'threePointersAttempted': stats.three_pointers_attempted,
                    'shots': shots_data
                }
                player_summary['games'].append(game_data)

            return Response(player_summary)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)
