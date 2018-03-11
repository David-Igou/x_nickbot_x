from riotwatcher import RiotWatcher

class Player:

    summonerId = ''
    summonerName = ''
    accountId = ''
    region = ''
    rank = ''
    gameSet = []
    gameIds = []
    rankedInfo = []
    watcher = RiotWatcher('f')

    def __init__(self, summonerName, region, token):
        self.summonerName=summonerName
        self.region = region
        self.watcher = RiotWatcher(token)
        self.getPlayerInfo(summonerName)
        self.getRankedInfo()

    def getPlayerInfo(self, summonerName):
        query = self.watcher.summoner.by_name(self.region, summonerName)
        self.accountId = query["accountId"]
        self.summonerId = str(query["id"])

    def getRankedInfo(self):
        self.rankedInfo = self.watcher.league.positions_by_summoner(self.region, self.summonerId)
        print(len(self.rankedInfo))
        if(len(self.rankedInfo)>0):
            self.rank = self.rankedInfo[0]['tier'] + " " + self.rankedInfo[0]['rank']

    def summary(self):
        return("Username: " + self.summonerName + " With Summoner ID: " + self.summonerId + " They are currently ranked: " + self.rank)
