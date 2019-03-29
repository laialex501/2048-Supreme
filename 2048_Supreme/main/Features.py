import Game_World
import numpy as np

class Features:
    """
    Class for acquiring features for our game
    """

    def __init__(self):
        """
        features: a list of our feature functions
        """
        self.features = []

    def getFeatures(self):
        return self.features

class Features_2048(Features):
    """
    Features specific to the game 2048 Supreme
    """

    def __init__(self, game=Game_World.Game_2048()):
        """
        Initializes our features list.
        
        features: a list of our feature functions
        GAME: a dummy instance of 2048 or a specific game to customize features for
        """
        self.features = [self.maxTile, self.increaseTile, self.adjacentTile,
                       self.score, self.numTiles, self.reducedTiles, self.isGoal]
        self.GAME = game

    def maxTile(self, state, action):
        """
        Returns the expected maximum tile of the next state
        """
        board = self.GAME.get_successor(state, action)
        return float(np.amax(board))

    def increaseTile(self, state, action):
        """
        Returns 1 if we are expected to increase our maximum tile
        """
        board = self.GAME.get_successor(state, action)
        
        maxOld = np.amax(state)
        maxNew = np.amax(board)
        if maxNew > maxOld:
            return 1.0
        else:
            return 0.0

    def adjacentTile(self, state, action):
        """
        The value of the two maximum adjacent tiles in the new state
        """
        board = self.GAME.get_successor(state, action)
        
        maxAdj = 0.0
        n = len(board[0])
        m = len(board)
        for col in range(n):
            for row in range(m):                
                if (col+1 < n) and (board[row][col+1] == board[row][col]):
                    maxAdj = max(maxAdj, board[row][col])
                if (row+1 < m) and (board[row+1][col] == board[row][col]):
                    maxAdj = max(maxAdj, board[row][col])
        return float(maxAdj)

    def score(self, state, action):
        """
        The expected score of the next state
        """
        board = self.GAME.get_successor(state, action)
        
        score = 0.0
        for tile in np.nditer(board):
            score += tile
        return score

    def numTiles(self, state, action):
        """
        Returns the expected number of tiles in our next state
        """
        board = self.GAME.get_successor(state, action)
        
        tiles = 0.0
        for tile in np.nditer(board):
            if tile != 0:
                tiles += 1
        return tiles
    
    def reducedTiles(self, state, action):
        """
        Returns the difference between the number of tiles in 
        our old state and the number of tiles in the next state
        """
        tilesOld = 0.0
        for tile in np.nditer(state):
            if tile != 0:
                tilesOld += 1
        
        tilesNew = self.numTiles(state, action)
        
        return tilesNew - tilesOld
    
    def isGoal(self, state, action):
        """
        Returns 1 if we reach our goal in the next state
        """
        goal = self.GAME.get_goal()
        board = self.GAME.get_successor(state, action)
        
        for tile in np.nditer(board):
            if tile >= goal:
                return 1.0
        return 0.0
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, key):
        return self.features[key]
    
def testFeatures():
    state = np.array([[2, 4, 8, 16],
                      [2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 2048]])
    action = "up"
    print(state)
    
    f = Features_2048()
    feat = f.getFeatures()
    f_vec = []
    
    for feature in feat:
        f_vec.append(feature(state, action))
    print(f_vec)
        