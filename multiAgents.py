# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Let us consider our logic be heuristic initially assigned 0
        heuristic = 0

        #maintain a data structure to store Distance to ghost from pacman
        DistanceToGhost = []

        #maintain a data structure to store distance to Food from pacman pos
        DistanceToFood = []

        #Creating the foodlist that needs to be taken care in the evaluation function to compute distance to food from pacman
        FoodList = newFood.asList()

        #Now computing the distance using manhattan distance our heuristic between ghost and pacman
        for ghost in newGhostStates:

            # Compute the list of Distances of Ghost from the pacman , later used to find the minimum needed in heuristic
            DistanceToGhost = DistanceToGhost + [manhattanDistance(ghost.getPosition(), newPos)]

        #Similarly we compute distance to each food from pacman position.
        for food in FoodList:

            # Compute the list of Distances of food from the pacman , later used to find the minimum needed in heuristic
            DistanceToFood = DistanceToFood + [manhattanDistance(newPos, food)]

        #considering a variable to make a food factor less
        FoodFactorLess = 0

        #as stated in the writeup, we consider the fraction of min Distance to food to increase the probability of eating that food
        if len(DistanceToFood) > 0:
            FoodFactorLess = 1/(min(DistanceToFood))

        #here our heuristic checks, if distance to ghost is less than 2, that is Ghost is near that radius, we assigne our heuristic
        #some large negative value so it doesnt meet the ghost
        if min(DistanceToGhost) < 2:
            heuristic = -10000000
        else:

            #Our heuristic keeps adding the fraction of min distance to ghost and fraction of distance to food.
            # we do this, as we want maximum distance to ghost and eat food quickly with minimum distance to food.
            heuristic += (min(DistanceToGhost) * FoodFactorLess)

        #return the cumulative heuristic by adding the default getScore which program was returning by default.
        #we consider this as our new heuristic are calculated and hence to be added to previous score
        return heuristic + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        #as specified above , we compute number of agent's
        TotalAgents=gameState.getNumAgents()

        #As we know, pac man is only one, so we can compute ghost
        TotalGhost=TotalAgents-1

        # When pac man turn is to move, we are at depth 0. So we define a constant for it to pass it in function later
        Depth = 0

        #we specify ghost agent index variable as one, initialisation done. Passed inside the function.
        ghost_index=1

        # we declare a local variable temp score to count up the maximum score and use it to present bestScore
        temp_score=0

        # Computing legal moves for pac man by specifying agent index as 0.
        LegalMoves=gameState.getLegalActions(0)

        #To increase search depth achievable by our agent Pac man(agent index==0) mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalMoves:
            LegalMoves.remove(Directions.STOP)

        #Here, we compute the each legal move and pass the successor for that legal move in Min Val.
        # So, here our ghost_index=1(at depth =0 ) ghost needs to move now.we pass TotalGhost as a parameter to check later in function
        #this is recursive function, so it will compute all possible states on Depth 0, for ghost 1,2,3 and then increase depth.
        for moves in LegalMoves:
            scores = [self.MinVal(gameState.generateSuccessor(0,moves),ghost_index,Depth,TotalGhost)]

            #Here, we keep replacing the best Score that is the maximum value to store it in temp_score.
            # finally, for max score we get a best move, which we are getting from the above.
            if temp_score < scores:
                temp_score=scores
                bestMove=moves

        #Here we return the best move as an action .
        return bestMove

    #Here, we define our MinVal function which is used above for ghost
    def MinVal(self,GameState,agentIndex,Depth,TotalGhost):

        #now we see whether game state is reached to win or lose, if yes then return the default evaluation function
        if GameState.isLose() or GameState.isWin() or Depth == self.depth:
            return self.evaluationFunction(GameState)

        # getting the legal actions for ghost based on the agent index, where it is >= 1 that is ghost.
        # as we pass 1 as an index from above, so for first iteration it runs for first ghost.
        LegalActions = GameState.getLegalActions(agentIndex)

        #To increase search depth mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalActions:
            LegalActions.remove(Directions.STOP)

        # computing successor for ghost based on index and action.
        for actions in LegalActions:
            nextGhostState = [GameState.generateSuccessor(agentIndex,actions)]

        # now, this condition occurs, when we are on depth 0, pac man has made one move, ghost turn is to move and it moves for
        # all the ghost until it becomes equal to TotalGhost value. As ghost is moving we recursively call this min function
        # and each time index is incremented to got to next ghost until it equals all the ghost
        if agentIndex < TotalGhost:
            for states in nextGhostState:
                return min([self.MinVal(states,agentIndex+1,Depth,TotalGhost)])

        # otherwise, when we cover all the ghost, we are done on depth 0, we call Max function for pacman on the depth 1 and so on
        # So, here we keep incrementing depth, whenever we reach all the ghost on a single level, its time to move on another one
        elif agentIndex == TotalGhost:
            for states in nextGhostState:
                return min([self.MaxVal(states,0,Depth+1,TotalGhost)])

        #we return min value of the scores receive in this function above in each iteration.

    # here we define our MaxVal function used above for pac man.
    def MaxVal(self,GameState,agentIndex,Depth,TotalGhost):

        #now we see whether game state is reached to win or lose, if yes then return the default evaluation function, same as in minimum function
        if GameState.isLose() or GameState.isWin() or Depth == self.depth:
            return self.evaluationFunction(GameState)

        # getting the legal actions for pac man based on the agent index, where it is now 0 as passed above in min function.
        # keep in mind, at each iteration, depth changes to 1,2... till we specify depth for pac man and index remain 0 only.
        LegalActions = GameState.getLegalActions(agentIndex)

        #To increase search depth mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalActions:
            LegalActions.remove(Directions.STOP)

        # computing successor for pac man based on index and action.as in function above we pass agent Index as 0 for max(that is pacman)
        for actions in LegalActions:
            nextPacState = [GameState.generateSuccessor(agentIndex,actions)]

        # now for each state in the successor of pac man, we compute the recursive Min function for ghost.
        # note: Here we keep agent index=1, that is for pac man position first ghost is computed and then it is incremented in Min val each time
        # As it is max function, we return max value for pac man
        for nextState in nextPacState:
            return max([self.MinVal(nextState,1,Depth,TotalGhost)])

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # this piece of code is same as mini max with introduction alpha and beta components

        #as specified above , we compute number of agent's
        TotalAgents=gameState.getNumAgents()

        #As we know, pac man is only one, so we can compute ghost
        TotalGhost=TotalAgents-1

        # When pac man turn is to move, we are at depth 0. So we define a constant for it to pass it in function later
        Depth = 0

        #we specify ghost agent index variable as one, initialisation done. Passed inside the function.
        ghost_index=1

        # assigning alpha and beta the default infinite large and small values to use them later for comparing.
        # as used in the class slides  by the professor in the example.
        alpha = float('-inf')
        beta = float('inf')

        # Computing legal moves for pac man by specifying agent index as 0.
        LegalMoves=gameState.getLegalActions(0)

        #To increase search depth achievable by our agent Pac man(agent index==0) mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalMoves:
            LegalMoves.remove(Directions.STOP)

        # we declare a local variable temp score to minus infinity in order to compare with the scores obtained below
        temp_score=float('-inf')

        # We define this case in order to assign when score is much larger than beta.
        bestMove = LegalMoves[0]

        #Here, we compute the each legal move and pass the successor for that legal move in Min Val.
        #So, here our ghost_index=1(at depth =0 ) ghost needs to move now.we pass TotalGhost as a parameter to check later in function
        #this is recursive function, so it will compute all possible states on Depth 0, for ghost 1,2,3 and then increase depth.
        for moves in LegalMoves:
            scores = self.MinVal(gameState.generateSuccessor(0,moves),ghost_index,Depth,TotalGhost,alpha,beta)

            #Here, we keep replacing the best Score that is the maximum value to store it in temp_score.
            # finally, for max score we get a best move, which we are getting from the above.
            if scores > temp_score:
                temp_score = scores
                bestMove = moves

            # it is a check, which should not happen at root when score becomes more than infinity, so we return bestMove defined above
            if scores > beta:
                return bestMove

            #Here, we have to keep updating the alpha, with the maximum value, as we know we have to increase it from minus infinity
            alpha = max(alpha, scores)

        #Here we return the best move as an action .
        return bestMove

    #Here, we define our MinVal function which is used above for ghost
    def MinVal(self,GameState,agentIndex,Depth,TotalGhost,alpha,beta):

        #now we see whether game state is reached to win or lose, if yes then return the default evaluation function
        if GameState.isLose() or GameState.isWin() or Depth == self.depth:
            return self.evaluationFunction(GameState)

        # getting the legal actions for ghost based on the agent index, where it is >= 1 that is ghost.
        # as we pass 1 as an index from above, so for first iteration it runs for first ghost.
        LegalActions = GameState.getLegalActions(agentIndex)

        # We define this to compare it with the value received from the min val and max val functions
        score = float('inf')

        #To increase search depth mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalActions:
            LegalActions.remove(Directions.STOP)

        # computing successor for ghost based on index and action.
        for actions in LegalActions:
            nextGhostState = GameState.generateSuccessor(agentIndex,actions)

            # now, this condition occurs, when we are on depth 0, pac man has made one move, ghost turn is to move and it moves for
            # all the ghost until it becomes equal to TotalGhost value. As ghost is moving we recursively call this min function
            # and each time index is incremented to got to next ghost until it equals all the ghost
            # passing alpha and beta and storing the min value in score to compare later
            if agentIndex < TotalGhost:
                score = min(score, self.MinVal(nextGhostState,agentIndex+1,Depth,TotalGhost,alpha,beta))

            # otherwise, when we cover all the ghost, we are done on depth 0, we call Max function for pacman on the depth 1 and so on
            # So, here we keep incrementing depth, whenever we reach all the ghost on a single level, its time to move on another one
            # passing alpha and beta and storing the min value in score to compare later
            elif agentIndex == TotalGhost:
                score = min(score, self.MaxVal(nextGhostState,0,Depth+1,TotalGhost,alpha,beta))

            # condition checks, whether score is less than alpha as it does in the book algorithm, if yes, it returns that score
            if score < alpha:
                return score

            #if not, we keep replacing the infinitely large value initially with minimum score, then whosoever is minimum in next iteration
            # it replaces the value of beta, and hence we return that minimum value
            beta=min(score, beta)

        #return the score computed back to agent
        return score

    # here we define our MaxVal function used above for pac man.
    def MaxVal(self,GameState,agentIndex,Depth,TotalGhost,alpha,beta):

        #now we see whether game state is reached to win or lose, if yes then return the default evaluation function, same as in minimum function
        if GameState.isLose() or GameState.isWin() or Depth == self.depth:
            return self.evaluationFunction(GameState)

        # getting the legal actions for pac man based on the agent index, where it is now 0 as passed above in min function.
        # keep in mind, at each iteration, depth changes to 1,2... till we specify depth for pac man and index remain 0 only.
        LegalActions = GameState.getLegalActions(agentIndex)

        # We define this to compare it with the value received from the min val functions
        score = float('-inf')

        #To increase search depth mentioned in write up, we remove the STOP direction from list of legal moves
        # So, if it exist, remove from legal moves
        if Directions.STOP in LegalActions:
            LegalActions.remove(Directions.STOP)

        # computing successor for pac man based on index and action.as in function above we pass agent Index as 0 for max(that is pacman)
        for actions in LegalActions:
            nextPacState = GameState.generateSuccessor(agentIndex,actions)

        # Computing and comparing the scores and returning maximum for pac man
        # note: Here we keep agent index=1, that is for pac man position first ghost is computed and then it is incremented in Min val each time
        # As it is max function, we return max value for pac man
            score = max(score,self.MinVal(nextPacState,1,Depth,TotalGhost,alpha,beta))

            # condition checks, whether score is greater than beta as it does in the book algorithm, if yes, it returns that score
            if score > beta :
                return score

            #if not, we keep replacing the infinitely small value initially with maximum score, then whosoever is maximum in next iteration
            # it replaces the value of alpha, and hence we return that maximum value
            alpha=max(alpha,score)

        #return the score computed back to agent
        return score

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

