class Game:
    def __init__(self, tournament, opponent):
        self.tournament = tournament
        self.opponent = opponent
        self.pointsPlayed = 0
        self.pulls = []
        self.goals = 0
        self.assists = 0 
        self.assistsToAssists = 0
        self.catches = 0
        self.plusMinus = 0
        self.throwaways = 0
        self.drops = 0
        self.ds = 0
        self.ogPlusMinus = 0
        self.completions = 0
    def changeOGPM(self, num):
        self.ogPlusMinus += num
    def incrPP(self):
        self.pointsPlayed += 1
    def incrPulls(self, pull):
        self.pulls.append(pull)
    def incrAssists(self):
        self.assists += 1
    def incrGoals(self):
        self.goals += 1
    def incrCatches(self):
        self.catches += 1
    def changePM(self, num):
        self.plusMinus += num
    def incrATOA(self):
        self.assistsToAssists += 1
    def incrDs(self):
        self.ds += 1
    def incrDrops(self):
        self.drops += 1
    def incrThrowaways(self):
        self.throwaways += 1
    def incrCompletions(self):
        self.completions += 1
    def __eq__(self, other):
        return self.tournament == other.tournament and self.opponent == self.opponent
    def __str__(self): 
        return f'Tournament: {self.tournament} Game: {self.opponent}'
    def __repr__(self):
        return f'Tournament: {self.tournament} Game: {self.opponent}'