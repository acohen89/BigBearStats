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
        self.completions = 0


    def incrPP(self):
        self.pointsPlayed += 1
    def incrPulls(self, pull):
        self.pulls.append(pull)
    def incrAssists(self):
        self.assists += 1
    def incrGoals(self):
        self.goals += 1
    def __eq__(self, other):
        return self.tournament == other.tournament and self.opponent == self.opponent
    def __str__(self): 
        return f'Tournament: {self.tournament} Game: {self.opponent}'
    def __repr__(self):
        return f'Tournament: {self.tournament} Game: {self.opponent}'