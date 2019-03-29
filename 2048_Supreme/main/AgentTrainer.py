from Game_World import *
from Agents import *
from Util import *
from Features import *

class AgentTrainer:
    """
    Trains a 2048 agent by running episodes
    """

    def __init__(self, alpha=0.5, epsilon=0.05, gamma=0.8, maxEpisodes=10, features=[], rewardFunc=lambda: 0, 
              game=Game_2048, alpha_scaling=0.5, epsilon_scaling=0.5, alpha_scaling_interval=0.2, 
              epsilon_scaling_interval=0.2):
        """
        Takes in a game and creates an agent for it. Then trains that agent with
        the given parameters.

        Attributes:
        -----------
        alpha: the learning rate of the agent
        epsilon: the probability of taking a random action
        gamma: the discount factor on future rewards
        features: the feature functions used by this agent
        maxEpisodes: the number of episodes this agent will be trained on
        game: the game that this agent will train for
        alpha_scaling: the amount that we will scale our alphas by as we perform episodes
        epsilon_scaling: the amount that we will scale our epsilons by as we performed episodes
        alpha_scaling_interval: the percentage of max_episodes complete before we scale alpha
        epsilon_scaling_interval: the percentage of max_episodes complete before we scale epsilon
        alpha_interval_current: the alpha interval we are currently on
        epsilon_interval_current: the epsilon interval we are currently on
        """
        self.agent = ReinforcementAgent(alpha, epsilon, gamma, maxEpisodes, features, rewardFunc, game)
        self.alpha_scaling = alpha_scaling
        self.epsilon_scaling = epsilon_scaling
        self.alpha_scaling_interval = alpha_scaling_interval
        self.epsilon_scaling_interval = epsilon_scaling_interval
        self.alpha_interval_current = 1
        self.epsilon_interval_current = 1
        self.GAME = game

    def runAgent(self):
        """
        Runs our agent on a given instance of our game (assuming it is the same
        as the game we trained on). Then returns the actions we decided to take.
        """
        raiseNotDefined()

    def trainAgent2048(self, m=4, n=4, prime=2, goal=2048, board_array=None):
        """
        Trains our agent until it finishes our required training with a game using
        the specified parameters
        """
        while self.agent.inTraining():
            print("Beginning episode {0}".format(self.agent.numEpisodes))
            self.adjustAgent()
            game = self.GAME(m=m, n=n, prime=prime, goal=goal, board_array=board_array)
            self.agent.runEpisode(game)

    def adjustAgent(self):
        """
        Adjusts our agent's alpha and epsilon values if they have completed the
        specified percentage of their max episodes
        """
        episodes = self.agent.numEpisodes
        max_episodes = self.agent.maxEpisodes
        if max_episodes * self.alpha_scaling_interval * self.alpha_interval_current < episodes:
            new_alpha = self.agent.alpha * self.alpha_scaling
            self.agent.adjustAlpha(new_alpha)
            self.alpha_interval_current += 1
        if max_episodes * self.epsilon_scaling_interval * self.epsilon_interval_current < episodes:
            new_epsilon = self.agent.epsilon * self.epsilon_scaling
            self.agent.adjustEpsilon(new_epsilon)
            self.epsilon_interval_current += 1
            
    def getAgent(self):
        """
        Gets our agent
        """
        return self.agent
    
def rewardFunc1(startState, action, nextState):
    startScore = np.sum(startState)
    nextScore = np.sum(nextState)
    return nextScore-startScore

def testAgentTrainer():
    game = Game_2048(m=4, n=4, prime=2, goal=2048, board_array=None)
    f = Features_2048(game)
    features = f.getFeatures()
    trainer = AgentTrainer(alpha=0.5, epsilon=0.05, gamma=0.8, maxEpisodes=10, features=features, 
                           rewardFunc=rewardFunc1, game=Game_2048, alpha_scaling=0.5, epsilon_scaling=0.5, 
                           alpha_scaling_interval=0.2, epsilon_scaling_interval=0.2)
    trainer.trainAgent2048(m=4, n=4, prime=2, goal=2048, board_array=None)
    agent = trainer.getAgent()
    return agent

agent = testAgentTrainer()
print(agent.weights)

