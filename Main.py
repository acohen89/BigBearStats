from Player import *

def incrementPointsPlayed(curAction, players):
    playerColNames = ['Player 0', 'Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6']
    game = (curAction['Tournament'], curAction.name)
    for playerCol in playerColNames:
        players[curAction[playerCol]].incrPP(game)
    return players
def getAttributes(curAction):
    name = curAction.name
    game = (curAction['Tournament'], curAction.name)
    line = curAction['Line']
    eventType = curAction['Event Type']
    action = curAction['Action']
    passer = curAction['Passer']   
    receiver = curAction['Receiver']   
    defender = curAction['Defender']   
    hangTime = curAction['Hang Time (secs)']   
    player0 = curAction['Player 0']   
    player1 = curAction['Player 1']   
    player2 = curAction['Player 2']   
    player3 = curAction['Player 3']   
    player4 = curAction['Player 4']   
    player5 = curAction['Player 5']   
    player6 = curAction['Player 6']   
    ourScoreEOP = curAction['Our Score - End of Point']
    theirScoreEOP = curAction['Their Score - End of Point']
    return (name, game, line, eventType, action, passer, receiver, defender, hangTime, player0, player1, player2, player3, player4, player5, player6, ourScoreEOP, theirScoreEOP)  
def processActions(df, players):
    curOpponent = ''
    ourScore = 0
    theirScore = 0
    prevPasser = 'Anonymous'
    for row in range(len(df)):
        curAction = df.iloc[row]
        name, game, line, eventType, action, passer, receiver, defender, hangTime, player0, player1, player2, player3, player4, player5, player6, ourScoreEOP, theirScoreEOP = getAttributes(df.iloc[row])
        if name != curOpponent: ## new game
            curOpponent = name         
            ourScore = 0
            theirScore = 0
        if ourScoreEOP != ourScore: ## after this action, we scored
            ourScore = ourScoreEOP
            players = incrementPointsPlayed(curAction, players)
        elif theirScoreEOP != theirScore: ## after this action they score
            players = incrementPointsPlayed(curAction, players)
            theirScore = theirScoreEOP
        if defender != 'Anonymous':
            if action == 'Pull':
                players[defender].incrPulls(hangTime, game)
            elif action == 'PullOb':
                players[defender].incrPulls(0.0, game)
        if eventType == 'Offense':
            if action == 'Goal':
                players[passer].incrAssists(game)
                players[receiver].incrGoals(game)
                players[receiver].incrCatches(game)
                if passer != 'Anonymous':
                    players[passer].incrCmpltn(game)
                if prevPasser != 'Anonymous':
                    players[prevPasser].incrATOA(game)
                    ## Add to plus minus? 
            if action == 'Catch':
                players[receiver].incrCatches(game)
                prevPasser = passer
                if passer != 'Anonymous':
                    players[passer].incrCmpltn(game)
            if action == 'Throwaway' and passer != 'Anonymous':
                players[passer].incrThrowaways(game)
            if action == 'Drop':
                players[receiver].incrDrops(game)
        if eventType == 'Defense':
            if action == 'D':
                if defender != 'Anonymous':
                    players[defender].incrDs(game)
            

    return players