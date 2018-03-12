from riotwatcher import RiotWatcher
from stats import stats

class Player:

    summonerId = ''
    summonerName = ''
    accountId = ''
    region = ''
    rank = ''
    gameSet = []
    gameIds = []
    rankedInfo = []
    watcher = None

    def __init__(self, summonerName, region, token):
        self.summonerName=summonerName.replace("_"," ")
        self.region = region
        self.watcher = RiotWatcher(token)
        self.getPlayerInfo(self.summonerName)
        self.getRankedInfo()

    def getPlayerInfo(self, summonerName):
        query = self.watcher.summoner.by_name(self.region, summonerName)
        self.accountId = query["accountId"]
        self.summonerId = str(query["id"])
        self.summonerName = query["name"]

    def getRankedInfo(self):
        self.rankedInfo = self.watcher.league.positions_by_summoner(self.region, self.summonerId)
        if(len(self.rankedInfo)>0):
            self.rank = self.rankedInfo[0]['tier'] + " " + self.rankedInfo[0]['rank']

    def getLastGameIds(self):
        gameSums = self.watcher.match.matchlist_by_account_recent(self.region,self.accountId)
        for g_id in gameSums['matches']:
            self.gameIds.append(g_id['gameId'])

    def getLastGames(self):
        if(len(self.gameIds) == 0):
            self.getLastGameIds()
        for match in self.gameIds:
            self.gameSet.append(self.watcher.match.by_id(self.region,match))

    def getAllGames(self):
        return self.gameSet

    def getTotalDeaths(self):
        if(len(self.gameSet)<1):
            self.getLastGames()
        return(stats.total_deaths_in_games(self.gameSet,self.summonerName))

    def summary(self):
        return("Username: " + self.summonerName + " With Summoner ID: " + self.summonerId + " They are currently ranked: " + self.rank)
