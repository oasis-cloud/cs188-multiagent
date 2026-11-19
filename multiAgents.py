# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"
        # 没有食物或 ghost    
        if len(newFood.asList()) == 0:
            return successorGameState.getScore()
        # 靠近食物的权重越高
        food_distance = min([manhattanDistance(newPos, food) for food in newFood.asList()])
        food_weight = 1 / (1 if food_distance == 0 else food_distance)
        # 靠近 ghost 的权重越高
        ghost_distance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        ghost_weight = 1 / (1 if ghost_distance == 0 else ghost_distance) 
        
        # 当 PacMan 吃到 power pellet 时，食物的权重越高
        scaredTime = max(newScaredTimes)
        new_food_weight = food_weight * (1 if scaredTime == 0 else scaredTime)    

        return successorGameState.getScore() + new_food_weight - ghost_weight

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, agentIndex = 0, depth = self.depth):
            # 题目要求可以指定扩展的层级
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return (self.evaluationFunction(gameState), None)
            numAgents = gameState.getNumAgents()
            nextDepth = depth
            # 所有智能体走完一轮算 1 个 depth
            nextAgentIndex = (agentIndex + 1) % numAgents
            nextDepth = depth
            if nextAgentIndex == 0:
                nextDepth -= 1
            # 获取当前 Agent 的可用动作
            actions = gameState.getLegalActions(agentIndex)
            # 一轮博弈是 Pacman 先走，然后每个 Ghost 轮流走
            list = []
            for action in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                v = minimax(successorGameState, nextAgentIndex, nextDepth)
                list.append((v[0], action))
            if agentIndex == 0:
                # 求最大值
                maxValue = max(list, key=lambda x: x[0])
                return maxValue
            else:
                # 求最小值，也就是所有 ghost 求 minvalue
                minValue = min(list, key=lambda x: x[0])
                return minValue
        
        value = minimax(gameState)
        return value[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # alpha 初始为负无穷，是因为 max 取最大值，当进入第一个最大值检查时，要能保证第一个值赋值给 alpha，相当于 max(第一个值， -inf)
        # beta 初始为正无穷，是因为 min 取最小值，当进入第一个最小值检查时，要能保证第一个值赋值给 beta，相当于 min(第一个值， inf)
        def alphaBetaMinMax(gameState, agentIndex = 0, depth = self.depth, alpha = float('-inf'), beta = float('inf')):
            # 定义递归函数的终止条件
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return (self.evaluationFunction(gameState), None)
            # 此函数支持多智能体，所以要根据智能体数量计算 depth 的变化
            numAgents = gameState.getNumAgents()
            nextDepth = depth
            # 所有智能体走完一轮算 1 个 depth
            nextAgentIndex = (agentIndex + 1) % numAgents
            nextDepth = depth
            if nextAgentIndex == 0:
                nextDepth -= 1
            # 获取当前 Agent 的可用动作
            actions = gameState.getLegalActions(agentIndex)
            # 一轮博弈是 Pacman 先走，然后每个 Ghost 轮流走
            # 执行 min 的时候给 alpha 赋值，执行 max 的时候给 beta 赋值
            list = []
            for action in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                v = alphaBetaMinMax(successorGameState, nextAgentIndex, nextDepth, alpha, beta)
                print('alpha:', alpha, ' beta:', beta, ' agentIndex:', agentIndex, ' action:', action, ' v:', v[0])
                if agentIndex == 0:
                    # 求最大值，因为 PacMan 是 第一个，所以这里相当于在做 maxValue 的处理
                    alpha = max(alpha, v[0])
                    list.append((v[0], action))
                    if alpha > beta:
                        break
                else:
                    # 求最小值，也就是所有 ghost 求 minvalue
                    beta = min(beta, v[0])
                    list.append((v[0], action))
                    if alpha > beta:
                        print('min break:', alpha, beta, agentIndex, action, v[0])
                        break
            if agentIndex == 0:
                # 求最大值
                maxValue = max(list, key=lambda x: x[0])
                return maxValue
            else:
                # 求最小值，也就是所有 ghost 求 minvalue
                minValue = min(list, key=lambda x: x[0])
                return minValue

        value = alphaBetaMinMax(gameState)
        return value[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        def expectimax(gameState, agentIndex = 0, depth = self.depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return (self.evaluationFunction(gameState), None)
            numAgents = gameState.getNumAgents()
            nextDepth = depth
            nextAgentIndex = (agentIndex + 1) % numAgents
            nextDepth = depth
            if nextAgentIndex == 0:
                nextDepth -= 1
            # 预期最大值是对状态转移的概率做评估
            # successors = gameState.getLegalSuccessors(agentIndex)
            actions = gameState.getLegalActions(agentIndex)
            list = []

            for action in actions:
                successorGameState = gameState.generateSuccessor(agentIndex, action)
                value = expectimax(successorGameState, nextAgentIndex, nextDepth)
                if agentIndex == 0:
                    list.append((value[0], action))
                else:
                    expectedValue = value[0] + value[0] * (1 / len(actions))
                    list.append((expectedValue, action))
            
            if agentIndex == 0:
                maxValue = max(list, key=lambda x: x[0])
                return maxValue
            else:
                minValue = sum(x[0] for x in list)
                # 预期值实际上是一个虚拟节点。action 实际是通过 max 计算得出来的。
                return (minValue, None)

        value = expectimax(gameState)
        return value[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    # 没有食物或 ghost    
    if len(newFood.asList()) == 0:
        return currentGameState.getScore()
    # 靠近食物的权重越高
    fen = 20
    food_distance = min([manhattanDistance(newPos, food) for food in newFood.asList()])
    food_weight = 0
    if food_distance == 0:
        food_weight = fen
    else:
        food_weight = fen * (1 / food_distance)
    # 胶囊距离
    capsules = currentGameState.getCapsules()
    if len(capsules) > 0:
        capsule_distance = min([manhattanDistance(newPos, capsule) for capsule in capsules])
        if capsule_distance == 0:
            capsule_weight = fen
        else:
            capsule_weight = fen * (1 / capsule_distance)
    else:
        capsule_weight = 0
    # 靠近 ghost 的权重越高
    ghost_distance = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
    if ghost_distance == 0:
        ghost_weight = 99999
    else:
        ghost_weight = fen * (1 / ghost_distance)
    
    # 当 PacMan 吃到 power pellet 时，食物的权重越高
    scaredTime = max(newScaredTimes)
    new_food_weight = food_weight * (1 if scaredTime == 0 else scaredTime)    

    return currentGameState.getScore() + new_food_weight + capsule_weight - ghost_weight

# Abbreviation
better = betterEvaluationFunction
