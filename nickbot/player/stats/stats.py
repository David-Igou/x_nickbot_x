def player_deaths_in_game(game, player):
    playerid = ''
    for players in game['participantIdentities']:
        if(players['player']['summonerName'] == player):
            playerid=players['participantId']
    for players in game['participants']:
        if(players['participantId'] == playerid):
            return players['stats']['deaths']

def total_deaths_in_games(games,player):
    deaths=0
    for game in games:
        deaths = deaths + player_deaths_in_game(game,player)
    return deaths
