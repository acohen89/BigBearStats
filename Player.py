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
        return 1 - (self.throwaways / (self.completions + self.throwaways))
    def numberGamesPlayed(self):
        return len(self.games)
    def calcChanceOfScoring(self):
        if self.opsToScore == 0.0:
            return 0.0
        return self.pointsWhenPlaying / self.opsToScore
    def calcBreakChance(self):
        if self.DPointsPlayed == 0:
            return 0.0
        return self.numBreaks / self.DPointsPlayed
    def calcBrokenChance(self):
        if self.OPointsPlayed == 0:
            return 0.0
        return self.numBroken / self.OPointsPlayed
    
    def __init__(self, name):
        self.name = name
        self.pointsPlayed = 0
        self.pulls = []
        self.goals = 0
        self.pointsWhenPlaying = 0
        self.assists = 0 
        self.assistsToAssists = 0
        self.catches = 0
        self.ogPlusMinus = 0
        self.plusMinus = 0
        self.opsToScore = 0
        self.OPointsPlayed = 0
        self.DPointsPlayed = 0
        self.numBreaks = 0
        self.numBroken = 0
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
        self.chanceOfScoring = self.calcChanceOfScoring()
        self.breakChance = self.calcBreakChance()
        self.brokenChance = self.calcBrokenChance()
        # computable variables are the following:
        # avgPullHangtime, obPulls, catchingPercent, passingPercent, 
    def checkForGame(self, game):
        if game not in self.games: 
            self.games.update({game: Game(game[0], game[1])})
    def incrNumBreaks(self):
        self.numBreaks += 1
        self.breakChance = self.calcBreakChance()
    def incrNumBroken(self):
        self.numBroken += 1
        self.brokenChance = self.calcBrokenChance()
    def incrOPointsPlayed(self):
        self.OPointsPlayed +=1
        self.brokenChance = self.calcBrokenChance()
    def incrOpsToScore(self):
        self.opsToScore += 1
    def incrDPointsPlayed(self):
        self.DPointsPlayed +=1
        self.breakChance = self.calcBreakChance()
    def incrPP(self, game):
        self.pointsPlayed += 1
        self.checkForGame(game)
        self.games[game].incrPP()
    def changePM(self, game, num):
        self.checkForGame(game)
        self.plusMinus += num
        self.games[game].changePM(num)
    def incrAssists(self, game):
        self.checkForGame(game)
        self.assists += 1   
        self.games[game].incrAssists()
    def incrATOA(self, game):
        self.assistsToAssists += 1 
        self.checkForGame(game)
        self.games[game].incrATOA()
    def incrGoals(self, game):
        self.checkForGame(game)
        self.games[game].incrGoals()
        self.goals += 1   
    def incrCompletions(self, game):
        self.checkForGame(game)
        self.completions += 1
        self.games[game].incrCompletions()
        self.catchingPercent = self.calcCatchingPercent()
    def changeOGPM(self, game, num):
        self.checkForGame(game)
        self.ogPlusMinus += num
        self.games[game].changeOGPM(num)
    def incrPulls(self, pull, game):
        if pull == 0.0:
            self.obPulls += 1
        self.pulls.append(pull)
        self.checkForGame(game)
        self.games[game].incrPulls(pull)
        self.avgPullHangtime = self.avgeragePullHangtime()
    def incrDrops(self, game):
        self.drops += 1
        self.checkForGame(game)
        self.catchingPercent = self.calcCatchingPercent()
        self.games[game].incrDrops()
    def incrCatches(self, game):
        self.checkForGame(game)
        self.catches += 1
        self.games[game].incrCatches()
        self.catchingPercent = self.calcCatchingPercent()
    def incrOpsToScore(self):
        self.opsToScore += 1
        self.chanceOfScoring = self.calcChanceOfScoring()
    def incrThrowaways(self, game):
        self.throwaways += 1
        self.checkForGame(game)
        self.games[game].incrThrowaways()
        self.passingPercent = self.calcPassingPercent()
    def incrCmpltn(self, game):
        self.completions += 1
        self.checkForGame(game)
        self.games[game].incrCompletions()
        self.passingPercent = self.calcPassingPercent()
    def incrGamesPlayed(self, game, tournament):
        self.gamesPlayed.update({tournament: game})
    def incrDs(self, game):
        self.ds += 1
        self.checkForGame(game)
        self.games[game].incrDs()
    def incrPointsWhenPlaying(self):
        self.pointsWhenPlaying += 1
        self.chanceOfScoring = self.calcChanceOfScoring()
    def incrCompletions(self):
        self.completions += 1
    def __eq__(self, other):
        return self.name == other.name
    def __str__(self): 
        return self.name
    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))