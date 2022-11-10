import pandas as pd 
import numpy as np
from Player import *
from Main import *
import unittest


class Test(unittest.TestCase):
    pd.set_option('display.precision', 2)
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('BigBearStats.csv', index_col=2)
    lp = 'Porbter Lot'
    badColumns = ['Date/Time', 'Point Elapsed Seconds','Player 7', 'Player 8', 
            'Player 9', 'Player 10', 'Player 11', 'Player 12', 'Player 13', 'Player 14', 
            'Player 15', 'Player 16', 'Player 17', 'Player 18', 'Player 19', 'Player 20', 
            'Player 21', 'Player 22', 'Player 23', 'Player 24', 'Player 25', 'Player 26', 
            'Player 27', 'Elapsed Time (secs)', 'Begin X', 'Begin Y', 'End X', 'End Y', 
            'Distance Unit of Measure', 'Absolute Distance', 'Lateral Distance', 'Toward Our Goal Distance', 'Begin Area', 'End Area']
    def getPlayers(df):
        players = {}
        playerColNames = ['Player 0', 'Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6']
        for col in playerColNames:
            for playerName in df[col]:
                curPlayer = Player(playerName)
                players.update({playerName: curPlayer})
        return players
    df = df.drop(badColumns, axis=1)
    players = getPlayers(df) 
    playersDF = pd.DataFrame.from_records((vars(player) for player in list(players.values())), index='name')
    df = df.rename(columns={'Tournamemnt': 'Tournament'})
    players = processActions(df, players)
    playersDF = pd.DataFrame.from_records((vars(player) for player in list(players.values())), index='name')
    
    def testPointsPlayed(self):
        ## Testing total Points Played
        self.assertEqual(self.playersDF.loc[:,'pointsPlayed']['Blaze'], 76)
        self.assertEqual(self.playersDF.loc[:,'pointsPlayed']['Ochen'], 111)
        self.assertEqual(self.playersDF.loc[:,'pointsPlayed']['Ryan'], 4)
        self.assertEqual(self.playersDF.loc[:,'pointsPlayed']['Juice'], 47)
        self.assertEqual(self.playersDF.loc[:,'pointsPlayed']['Dreq'], 64)

        ## Testing points played by game
        self.assertEqual(self.playersDF.loc[:,'games']['Blaze'][('Cav Cup', 'Navy y')].pointsPlayed, 4)
        self.assertEqual(self.playersDF.loc[:,'games']['C^2'][('Porbter Lot', 'Dartmouth')].pointsPlayed, 11)
        self.assertEqual(self.playersDF.loc[:,'games']['Fondue'][('Showcase', 'NYU')].pointsPlayed 
            + self.playersDF.loc[:,'games']['Fondue'][('Cav Cup', 'Lehigh')].pointsPlayed, 20)

    def testPulls(self):
        ## By average over all games
        self.assertAlmostEqual(self.playersDF.loc[:,'avgPullHangtime']['Ren'], 5.16, 2)
        self.assertAlmostEqual(self.playersDF.loc[:,'avgPullHangtime']['Ochen'], 5.37, 2)
        self.assertAlmostEqual(self.playersDF.loc[:,'avgPullHangtime']['Gekken'], 5.39, 2)

        ## List of pulls per game
        self.assertEqual(self.playersDF.loc[:,'games']['Sam'][('Porbter Lot', 'Maine')].pulls,[5.913, 0.0])

        ## Test OB Pulls
        self.assertEqual(self.playersDF.loc[:,'obPulls']['Sam'], 7)
        self.assertEqual(self.playersDF.loc[:,'obPulls']['Jack'], 0)
        self.assertEqual(self.playersDF.loc[:,'obPulls']['Ian'], 2)

    def testGoals(self):
        ## Test total goals 
        self.assertAlmostEqual(self.playersDF.loc[:,'goals']['Ryan'], 0)
        self.assertAlmostEqual(self.playersDF.loc[:,'goals']['Gbar'], 1)
        self.assertAlmostEqual(self.playersDF.loc[:,'goals']['Dreq'], 17)

        ## Test goals in a game
        self.assertEqual(self.playersDF.loc[:,'games']['Billy'][('Showcase', 'NYU')].goals, 0)
        self.assertEqual(self.playersDF.loc[:,'games']['Fondue'][('Showcase', 'NYU')].goals, 5)
        self.assertEqual(self.playersDF.loc[:,'games']['Chris'][('Cav Cup', 'UVA')].goals, 1)

        ## Test goals in multiple games
        self.assertEqual(self.playersDF.loc[:,'games']['Zla'][('Showcase', 'NYU')].goals
        + self.playersDF.loc[:,'games']['Zla'][('Porbter Lot', 'Tufts')].goals 
        + self.playersDF.loc[:,'games']['Zla'][('Cav Cup', 'UVA')].goals , 2)
        self.assertEqual(self.playersDF.loc[:,'games']['Lebron'][('Porbter Lot', 'NEU')].goals
        + self.playersDF.loc[:,'games']['Lebron'][('Porbter Lot', 'Uconn')].goals, 0)

    def testAssists(self):
        ## Test total assists
        self.assertEqual(self.playersDF.loc[:,'assists']['Ochen'], 22)
        self.assertEqual(self.playersDF.loc[:,'assists']['Champagn'], 0)
        self.assertEqual(self.playersDF.loc[:,'assists']['Eddie'], 2)

        ## Test assists in a game
        self.assertEqual(self.playersDF.loc[:,'games']['Lebron'][('Cav Cup', 'Elon')].assists, 0)        
        self.assertEqual(self.playersDF.loc[:,'games']['Chris'][('Porbter Lot', 'Bowdoin')].assists, 1)        
        self.assertEqual(self.playersDF.loc[:,'games']['Ochen'][('Porbter Lot', 'Bowdoin')].assists, 2)  
          
    def testComletions(self):
        ## Test total completions 
        self.assertEqual(self.playersDF.loc[:,'completions']['Ochen'], 269)
        self.assertEqual(self.playersDF.loc[:,'completions']['Charlie'], 1)
        self.assertEqual(self.playersDF.loc[:,'completions']['Neil'], 10)

        ## Test completions in a game 
        self.assertEqual(self.playersDF.loc[:,'games']['Sam'][('Porbter Lot', 'Tufts')].completions, 15)        
        self.assertEqual(self.playersDF.loc[:,'games']['Eddie'][('Porbter Lot', 'Tufts')].completions, 0)        
        self.assertEqual(self.playersDF.loc[:,'games']['Fondue'][('Cav Cup', 'Navy x')].completions
        + self.playersDF.loc[:,'games']['Fondue'][('Cav Cup', 'UVA')].completions, 28)  
          
    def testThrowAways(self):
        ## Test total throwAways
        self.assertEqual(self.playersDF.loc[:,'throwaways']['Gekken'], 18)
        self.assertEqual(self.playersDF.loc[:,'throwaways']['Ian'], 8)
        self.assertEqual(self.playersDF.loc[:,'throwaways']['Lebron'], 1)

        ## Test throwAways in a game    
        self.assertEqual(self.playersDF.loc[:,'games']['Billy'][('Showcase', 'NYU')].throwaways, 2)        
        self.assertEqual(self.playersDF.loc[:,'games']['Neil'][('Cav Cup', 'Lehigh')].throwaways, 2)        
        self.assertEqual(self.playersDF.loc[:,'games']['Jack'][('Cav Cup', 'Lehigh')].throwaways
        + self.playersDF.loc[:,'games']['Jack'][('Porbter Lot', 'Bowdoin')].throwaways, 1)        

    def passingPercentage(self): 
        ## Test overall passingPercentage
        self.assertAlmostEqual(self.playersDF.loc[:,'passingPercent']['Blaze'], 0.84, 2)
        self.assertAlmostEqual(self.playersDF.loc[:,'passingPercent']['Neil'], 0.77, 2)
        self.assertAlmostEqual(self.playersDF.loc[:,'passingPercent']['Manny'], 1.0, 2)
  
    def testDrops(self):
        ## Test total drops
        self.assertEqual(self.playersDF.loc[:,'drops']['Fondue'], 10)
        self.assertEqual(self.playersDF.loc[:,'drops']['Booboo'], 1)
        self.assertEqual(self.playersDF.loc[:,'drops']['Gbar'], 0)

        ## Test drops in a game
        self.assertEqual(self.playersDF.loc[:,'games']['Blaze'][('Porbter Lot', 'Uconn')].drops, 2)        
        self.assertEqual(self.playersDF.loc[:,'games']['Dreq'][('Porbter Lot', 'Uconn')].drops, 2)        
        self.assertEqual(self.playersDF.loc[:,'games']['Manny'][('Porbter Lot', 'NEU')].drops
        + self.playersDF.loc[:,'games']['Manny'][('Showcase', 'NYU')].drops, 1)        

    def testDs(self):
        ## Test total Ds
        self.assertEqual(self.playersDF.loc[:,'ds']['Ochen'], 13)
        self.assertEqual(self.playersDF.loc[:,'ds']['Ian'], 7)
        self.assertEqual(self.playersDF.loc[:,'ds']['Zla'], 2)

        ## Test ds in a game
        self.assertEqual(self.playersDF.loc[:,'games']['Chris'][('Showcase', 'NYU')].ds, 1)        
        self.assertEqual(self.playersDF.loc[:,'games']['Billy'][('Showcase', 'NYU')].ds, 0)        
        self.assertEqual(self.playersDF.loc[:,'games']['C^2'][('Cav Cup', 'Elon')].ds
        + self.playersDF.loc[:,'games']['C^2'][('Porbter Lot', 'Maine')].ds, 3)        

    

unittest.main()