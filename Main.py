from Player import *

def incrementPointsPlayed(curAction, players):
    playerColNames = ['Player 0', 'Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6']
    game = (curAction['Tournament'], curAction.name)
    for playerCol in playerColNames:
        players[curAction[playerCol]].incrPP(game)
        if curAction['Event Type'] == 'Offense':
            players[curAction[playerCol]].incrOPointsPlayed()
        elif curAction['Event Type'] == 'Defense':
            players[curAction[playerCol]].incrDPointsPlayed()

    return players
def getAttributes(curAction):
    activePlayers = []
    name = curAction.name
    game = (curAction['Tournament'], curAction.name)
    line = curAction['Line']
    eventType = curAction['Event Type']
    action = curAction['Action']
    passer = curAction['Passer']   
    receiver = curAction['Receiver']   
    defender = curAction['Defender']   
    hangTime = curAction['Hang Time (secs)']   
    activePlayers.append(curAction['Player 0'])
    activePlayers.append(curAction['Player 2'])
    activePlayers.append(curAction['Player 2'])
    activePlayers.append(curAction['Player 3'])
    activePlayers.append(curAction['Player 4'])
    activePlayers.append(curAction['Player 5'])
    activePlayers.append(curAction['Player 6'])  
    ourScoreEOP = curAction['Our Score - End of Point']
    theirScoreEOP = curAction['Their Score - End of Point']
    return (name, game, line, eventType, action, passer, receiver, defender, hangTime, activePlayers, ourScoreEOP, theirScoreEOP)  
def processActions(df, players):
    curOpponent = ''
    ourScore = 0
    theirScore = 0
    startingEventType = ''
    pullHangtime = {}
    activePull = False
    activePullTime = 0.0
    newOpToScore = True
    prevPasser = 'Anonymous'
    for row in range(len(df)):
        curAction = df.iloc[row]
        name, game, line, eventType, action, passer, receiver, defender, hangTime, activePlayers, ourScoreEOP, theirScoreEOP = getAttributes(df.iloc[row])
        if startingEventType != eventType: 
            startingEventType = eventType
            if startingEventType == 'Offense':
              for player in activePlayers:
                players[player].incrOpsToScore()
        if name != curOpponent: ## new game
            curOpponent = name         
            ourScore = 0
            theirScore = 0
            startingEventType = eventType
        if ourScoreEOP != ourScore: ## after this action, we scored
            ourScore = ourScoreEOP
            activePull = False
            newOpToScore = True
            players = incrementPointsPlayed(curAction, players)
        elif theirScoreEOP != theirScore: ## after this action they score
            players = incrementPointsPlayed(curAction, players)
            theirScore = theirScoreEOP
            activePull = False
            newOpToScore = True
        if action == 'Goal' and line == 'D' and eventType == 'Offense':
            for player in activePlayers:
                players[player].incrNumBreaks()
        if action == 'Goal' and line == 'O' and eventType == 'Defense':
            for player in activePlayers:
                players[player].incrNumBroken()
        if defender != 'Anonymous':
            if action == 'Pull':
                players[defender].incrPulls(hangTime, game)
                activePullTime = hangTime
                pullHangtime[activePullTime] = False
                activePull = True
            elif action == 'PullOb':
                players[defender].incrPulls(0.0, game)
        if eventType == 'Offense':
            if newOpToScore:
                for player in activePlayers: 
                    players[player].incrOpsToScore()
                newOpToScore = False
            if action == 'Goal':
                players[passer].incrAssists(game)
                players[receiver].incrGoals(game)
                players[receiver].incrCatches(game)
                players[receiver].changePM(game, 1.0) ## They score, PM + 1
                players[passer].changePM(game, 0.8) ## They assist, PM + 0.8
                players[passer].changeOGPM(game, 1)
                players[receiver].changeOGPM(game, 1)
                for player in activePlayers: 
                    players[player].incrPointsWhenPlaying()
                    players[player].changePM(game, 0.15) ## They are on the field when we score, PM + 0.15
                if passer != 'Anonymous':
                    players[passer].incrCmpltn(game)
                if prevPasser != 'Anonymous':
                    players[prevPasser].incrATOA(game)
                    players[player].changePM(game, 0.33) ## Assist To Assist, PM +0.05
            elif action == 'Catch':
                players[receiver].incrCatches(game)
                prevPasser = passer
                if passer != 'Anonymous':
                    players[passer].incrCmpltn(game)
            elif action == 'Throwaway' and passer != 'Anonymous':
                players[passer].incrThrowaways(game)
                players[passer].changePM(game, -0.9)
                players[passer].changeOGPM(game, -1)
                for player in activePlayers: 
                    players[player].changePM(game, -0.1)
            elif action == 'Drop':
                players[receiver].incrDrops(game)
                players[receiver].changePM(game, -0.75)
                players[receiver].changeOGPM(game, -1)
                for player in activePlayers:
                    players[player].changePM(game, -0.05)
            elif action == 'Stall':
                players[passer].changePM(game, -1.0)
                players[passer].changeOGPM(game, -1)
        if eventType == 'Defense':
            if action == 'D' or action == 'Throwaway':
                if activePull:
                    pullHangtime[activePullTime] = True
                    activePull = False
                if action == 'D' and defender != 'Anonymous':
                    players[defender].incrDs(game)
                    players[defender].changePM(game, 0.9)
                    players[defender].changeOGPM(game, 1)
                    for player in activePlayers:
                        players[player].changePM(game, 0.05)
            elif action == 'Callahan':
                players[defender].changePM(game, 2)
                players[defender].changeOGPM(game, 2)
                for player in activePlayers:
                        players[player].changePM(game, 0.05)
    return (players, pullHangtime)