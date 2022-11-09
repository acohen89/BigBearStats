from Game import *

class Player:
    def avgeragePullHangtime(self):
        total = 0
        size = 0
        if len(self.pulls) == 0:
            return 0.0
        for pull in self.pulls: 
            if pull != 0.0:
                size += 1
                total += pull
        if size == 0:
            return 0.0
        return total/size
    def calcOBPulls(self):
        totalOB = 0
        for pull in self.pulls:
            if pull == 0.0:
                totalOB += 1
            return totalOB
    def calcCatchingPercent(self):
        if self.drops == 0: 
            return 0.0
        return (self.catches + self.drops) / self.drops
    def calcPassingPercent(self):
        if self.throwaways == 0:
            return 0.0
        return (self.completions + self.throwaways) / self.throwaways
    def numberGamesPlayed(self):
        return len(self.games)
    def __init__(self, name):
        self.name = name
        self.pointsPlayed = 0
        self.pulls = []
        self.goals = 0
        self.assists = 0 
        self.assistsToAssists = 0
        self.catches = 0
        self.plusMinus = 0
        self.throwaways = 0
        self.drops = 0
        self.games = {} # Follow format of '(Tournament, 'Team'): Game(Tournament, 'Team')
        self.ds = 0
        self.completions = 0
        self.obPulls = 0
        self.numGamesPlayed = self.numberGamesPlayed()
        self.avgPullHangtime = self.avgeragePullHangtime()
        self.passingPercent = self.calcPassingPercent()
        self.catchingPercent = self.calcCatchingPercent()
        # computable variables are the following:
        # avgPullHangtime, obPulls, catchingPercent, passingPercent, 
    def checkForGame(self, game):
        if game not in self.games: 
            self.games.update({game: Game(game[0], game[1])})
    def incrPP(self, game):
        self.pointsPlayed += 1
        self.checkForGame(game)
        self.games[game].incrPP()
    def incrAssists(self, game):
        self.checkForGame(game)
        self.assists += 1   
        self.games[game].incrAssists()
    def incrATOA(self):
        self.assistsToAssists += 1   
    def incrGoals(self, game):
        self.checkForGame(game)
        self.games[game].incrGoals()
        self.goals += 1   
    def incrPulls(self, pull, game):
        if pull == 0.0:
            self.obPulls += 1
        self.pulls.append(pull)
        self.checkForGame(game)
        self.games[game].incrPulls(pull)
        self.avgPullHangtime = self.avgeragePullHangtime()
    def incrDrops(self):
        self.drops += 1
    def incrCatches(self):
        self.catches += 1
    def incrThrowaways(self):
        self.throwaways += 1
    def incrDrops(self):
        self.drops += 1
    def incrGamesPlayed(self, game, tournament):
        self.gamesPlayed.update({tournament: game})
    def incrDs(self):
        self.ds += 1
    def incrCompletions(self):
        self.completions += 1
    def __eq__(self, other):
        return self.name == other.name
    def __str__(self): 
        return self.name
    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))
