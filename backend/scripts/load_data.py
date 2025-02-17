import json
import psycopg2

# Database connection parameters
DATABASE = "okc"
USER = "okcapplicant"
PASSWORD = "thunder"
HOST = "localhost"
PORT = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
cur = conn.cursor()

# Function to load teams
def load_teams(data):
    for team in data:
        cur.execute("INSERT INTO teams (id, name) VALUES (%s, %s)", (team['id'], team['name']))
    print("Teams loaded successfully.")

# Function to load players
def load_players(data):
    for player in data:
        cur.execute("INSERT INTO players (id, name, team_id) VALUES (%s, %s, %s)", (player['id'], player['name'], player.get('team_id', None)))
    print("Players loaded successfully.")

# Function to load games
def load_games(data):
    for game in data:
        cur.execute("INSERT INTO games (id, date, home_team_id) VALUES (%s, %s, %s)", (game['id'], game['date'], game['homeTeam']['id']))
    print("Games loaded successfully.")

# Function to load player stats and shots
def load_player_stats_and_shots(games_data):
    for game in games_data:
        for player in game['homeTeam']['players']:
            # Insert player stats and retrieve the last inserted id
            cur.execute(
                "INSERT INTO player_stats (game_id, player_id, is_starter, minutes, points, assists, offensive_rebounds, "
                "defensive_rebounds, steals, blocks, turnovers, defensive_fouls, offensive_fouls, free_throws_made, "
                "free_throws_attempted, two_pointers_made, two_pointers_attempted, three_pointers_made, "
                "three_pointers_attempted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (game['id'], player['id'], player['isStarter'], player['minutes'], player['points'], player['assists'],
                 player['offensiveRebounds'], player['defensiveRebounds'], player['steals'], player['blocks'],
                 player['turnovers'], player['defensiveFouls'], player['offensiveFouls'], player['freeThrowsMade'],
                 player['freeThrowsAttempted'], player['twoPointersMade'], player['twoPointersAttempted'],
                 player['threePointersMade'], player['threePointersAttempted'])
            )
            
            # Get the id of the last inserted player stats
            player_stats_id = cur.fetchone()[0]

            # Load shots
            for shot in player['shots']:
                cur.execute(
                    "INSERT INTO shots (player_stats_id, is_make, location_x, location_y) VALUES (%s, %s, %s, %s)",
                    (player_stats_id, shot['isMake'], shot['locationX'], shot['locationY'])
                )
    print("Player stats and shots loaded successfully.")

# Load data from JSON files
with open('teams.json') as teams_file:
    teams_data = json.load(teams_file)
    load_teams(teams_data)

with open('players.json') as players_file:
    players_data = json.load(players_file)
    load_players(players_data)

with open('games.json') as games_file:
    games_data = json.load(games_file)
    load_games(games_data)
    load_player_stats_and_shots(games_data)

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
print("Data loading completed successfully.")