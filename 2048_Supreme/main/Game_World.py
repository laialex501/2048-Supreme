import numpy as np
from random import *

class Game_2048: 
    """
    The board game 2048 Supreme.
    
    Attributes:
    -----------
    board: the game board
    m: height of the board
    n: width of the board
    goal: the target goal to win the game
    prime: the base number of the game
    game_over: 1 = game over, 0 = game ongoing
    win: whether or not we won
    actions: allowable actions at each timestep
    history: list of previous board states
    move_hist: list of the distances moved by tiles during previous states
        -most recent move_hist contains distance travelled to current state
    fill_history: list of the coordinates randomly filled by a number
    """
    board = np.zeros(4)
    m = 4
    n = 4
    goal = 2048
    prime = 2
    game_over = 0
    win = 0
    main_actions = ["left", "up", "right", "down"]
    actions = ["left", "up", "right", "down", '0', '1', '2', '3', 
               0, 1, 2, 3, "a", "w", "d", "s"]
    history = []
    move_history = []
    fill_history = []
    merge_history = []
    
    def __init__(self, m = 4, n = 4, prime = 2, goal = 2048, board_array = None):
        """
        Creates a new instance of the game. Sets up the board, prime number, and goal number. 
        
        By default, it creates a standard 4 x 4 board. 
        
        Inputs
        ------
        m = # rows or the height of the board
        n = # columns or the width of the board
        prime = the base prime number of this game
        goal = the goal number to achieve to win
        board_array = a custom np array to use as a board
        """ 
        # create initial board
        if board_array is None:
            self.m = int(m)
            self.n = int(n)
            self.board = np.zeros((self.m, self.n))
        else:
            self.board = board_array
            
        # set goal
        if self.goal == "Endless":
            self.goal = float('inf')
        else:
            self.goal = goal

        self.prime = prime
        self.score = 0
        self.game_over = False
        self.win = False
        self.history = []
        self.move_history = []
        self.fill_history = []
        self.merge_history = []
        self.board_state_changed = True
        self.filled_last_time = False
        
        for i in range(0, self.prime):
            self.board = self.fill_random_cell(self.board, self.prime)
        
    def fill_random_cell(self, board, prime):
        """
        Fills a random empty cell in the board with the prime value.
        
        Inputs
        ------
        board: board you want to fill a cell with
        prime: the prime number to fill in the board
        
        Outputs:
        --------
        modBoard: the modified board with a cell filled in
        """
        modBoard = np.copy(board)
        i, j = (modBoard == 0).nonzero()
        if i.size != 0:
            self.filled_last_time = True
            rnd = randint(0, i.size - 1)
            # i[rnd] is row=y, j[rnd] is col=x
            modBoard[i[rnd], j[rnd]] = prime
            self.fill_history.append((i[rnd], j[rnd]))
        else:
            self.filled_last_time = False
        return modBoard
            
    # deprecated function, no longer used! kept around for record purposes
    def get_successor_2(self, board):
        """
        Moves all blocks to the left in the given board 
        
        Proceeds by column, moving each item in the column as far left as possible individually.
        
        If a block encounters another block, then it stops unless they are the same block. If so,
        then it counts if we can add a number of those blocks together equal to prime. If so, then
        they are combined. 
        
        Then it fills a random cell on the board. Then checks if it is game over. If a cell could not
        be filled, then it is game over. 
        
        Inputs:
        -------
        board: the board you want to enact moveLeft on
        
        Outputs:
        --------
        modBoard: the left shifted board
        move_hist: a dict mapping old coords to new positions on modBoard
        
        """
        m, n = board.shape
        modBoard = np.copy(board)
        merged = np.zeros((m, n))
        # Our movement history. Note it uses inverse notation of (y, x) coords
        move_hist = {}
        
        # i is current column == x
        for i in range(n):
            # j is current row == y
            for j in range(m):
                # current = the tile we are currently shifting
                current = modBoard[j][i]
                # Do nothing to zero tiles
                if current == 0:
                    continue
                    
                # Use y, x to keep track of where we have shifted (j, i) to SO FAR
                y, x = j, i
                
                # Let k be the column to the LEFT of y that we are trying to shift to
                print([i-t for t in range(1, i+1)])
                for k in [i-t for t in range(1, i+1)]:
                    dest_tile = modBoard[j][k]
                    
                    # if left adjacent tile is 0, we can shift to it
                    # since current != 0 due to above if statement
                    if dest_tile == 0:
                        modBoard[j][k] = current
                        modBoard[y][x] = 0
                        y = j
                        x = k
                        # set our movement history to this place
                        move_hist[(j, i)] = (y, x)
                        continue
                        
                    # if left adjacent tile is not the same, or has been merged, 
                    # then we can't do anything
                    elif (dest_tile != current) or merged[j][i] == 1:
                        break
                        
                    # left adjacent tile IS the same and is NOT 0
                    # therefore we must check if a merge is allowed
                    else:
                        # count remembers how many of the same tile we've seen
                        # if we find (self.prime) of the same we can merge them
                        count = 1
                        combine = False
                        # remembers the locations we saw the same tile, 
                        # which we need to convert to 0 if we merge
                        # written in inverse notation (y, x)
                        zeros = [(y, x)]
                        
                        # let c be the column to the LEFT where we are forward checking
                        # for the presence of the same current tile
                        for c in [i-h for h in range(k, i+1)]: 
                            
                            # found another of the same tile
                            if modBoard[j][c] == current:
                                count += 1
                                
                                # we have found the exact number of tiles needed for merge
                                if count == self.prime: 
                                    # merge all the tiles we've found at location (j, c)
                                    modBoard[j][c] = current * self.prime
                                    # mark that we've merged here already
                                    merged[j][c] = 1
                                    
                                    for index in zeros:
                                        # replace marked locations with 0,
                                        # note that the tiles have moved to (j, c) during merge
                                        z_y = index[0]
                                        z_x = index[1]
                                        modBoard[z_y][z_x] = 0
                                        move_hist[(z_y, z_x)] = (j, c)
                                    break
                                    
                                # if we haven't found the required count, then we won't stop here
                                # so mark this location, (j, c), as a potential place to put a zero
                                zeros.append((j, c))
                                    
                            # if we find any non-current tile we must stop searching
                            else:
                                break
        return modBoard
    
    def move_left(self, board): 
        """
        Moves all blocks to the left in the given board 
        
        Proceeds by column vector, scanning and shifting the column vector until all items have been placed.
        
        If a block encounters another block, then it stops unless they are the same block. If so,
        then it counts if we can add a number of those blocks together equal to prime. If so, then
        they are combined. 
        
        Then it fills a random cell on the board. Then checks if it is game over. If a cell could not
        be filled, then it is game over. 
        
        Inputs:
        -------
        board: the board you want to enact moveLeft on
        
        Outputs:
        --------
        modBoard: the left shifted board
        merge_array: an array indicating where merges occured on the board
        move_hist: an array mapping original tiles to new positions on modBoard
        """
        
        def merge_vectors(start_index, index_1, index_2, board, merge_array, move_hist):
            """
            Merge two vectors by shifting vector_2 as far left as 
            possible into vector 1.
            
            Returns the new (vector_1, vector_2) after the shift is complete.
            
            Inputs:
            ------
            start_index: the original index of the vector being shifted
            index_1: the index of the first vector on the board
            index_2: the index of the second vector on the board
            board: the board that you are extracting the vectors from
            merge_array: a 2D array with 1 in entries where we are not allowed to merge
            move_dist: an array mapping each tile in the array to the distance it travelled
                        - uses inverse notation (y, x)
            
            Outputs:
            -------
            vec_1: the new vector 1 after merge
            vec_2: the new vector 2 after merge
            merge_array: an updated 2D array with 1 in entries where we are not allowed to merge
            move_dist: an updated array mapping each tile in the array to the distance travelled to
                        - uses inverse notation (y, x)
            """
            
            vec_1 = np.copy(board[:, index_1])
            vec_2 = np.copy(board[:, index_2])
            ill_merge_1 = np.copy(merge_array[:, index_1])
            ill_merge_2 = np.copy(merge_array[:, index_2])
            move_dist_copy = np.copy(move_hist)
            
            for i in range(len(vec_1)):
                # Nothing to shift
                if vec_2[i] == 0:
                    continue
                # Space available to shift into
                elif vec_1[i] == 0 and vec_2[i] != 0:
                    vec_1[i] = vec_2[i]
                    vec_2[i] = 0
                    # moved from index_2 -> index_1
                    # Uses inverse (y, x) notation
                    move_dist_copy[i][start_index] += 1
                    
                # Merge is possible
                # Check not just if equal but if a multiple of a recent prime
                # TODO: RECORD THE LOCATIONS OF THE (ORIGIN MOVED) -> (END MOVED)
                
                elif (vec_1[i] == vec_2[i]) and (ill_merge_1[i] == 0) and (ill_merge_2[i] == 0):
                    vec_1[i] = vec_2[i] + vec_1[i]
                    vec_2[i] = 0
                    ill_merge_1[i] = 1
                    # moved from index_2 -> index_1
                    move_dist_copy[i][start_index] += 1
                    
            merge_array[:, index_1] = ill_merge_1
            merge_array[:, index_2] = ill_merge_2
            return vec_1, vec_2, merge_array, move_dist_copy
        
        rows, columns = board.shape
        mod_board = np.copy(board)
        merge_array = np.zeros((rows, columns))
        move_dist = np.zeros((rows, columns))
        
        for col_index in range(columns):
            #column_vector = board[:, col_index] 
            for shift_index in range(col_index):
                index_1 = col_index-shift_index-1
                index_2 = col_index-shift_index
                # acquire newly merged vectors
                vec_1, vec_2, new_merge_array, new_move_dist = merge_vectors(col_index, index_1, index_2, 
                                                                             mod_board, merge_array, move_dist)
                # update our values with new ones
                mod_board[:, index_1] = vec_1
                mod_board[:, index_2] = vec_2
                merge_array = new_merge_array
                move_dist = new_move_dist
        return mod_board, move_dist, merge_array
                
    
    def get_action(self, command):
        """
        Takes in a varaible command and returns the corresponding action.
        
        Inputs:
        ------
        command: can be anything, from a number (0, 1, 2, 3) to a digit (left, up, right, down)
        
        Outputs:
        movement: a digit corresponding to the command; (0, 1, 2, 3) only
        """
        if command in self.actions:
            movement = self.actions.index(command) % 4
        else:
            movement = None
        return movement
    
    def move(self, command = 0):
        """
        Moves the board in the desired direction. Moving up, right, or down is just
        moving left on a rotated board. 
        
        Inputs:
        -------
        direction: The direction you wish to move, the following are all equivalent.
            "left" = '0' = 0
            "up" = '1' = 1
            "right" = '2' = 2
            "down" = '3' = 3
            
        Outputs:
        ------
        Returns true when the move is complete
        """
        if command in self.actions:
            board = np.copy(self.board)
            movement = self.get_action(command)
            if movement == None:
                print('Error, retrieved incorrect command')
                pass  
            # rotate board to perform left shift movement
            board = np.rot90(board, movement)
            # find desired values from movement operation
            board, move_dist, merge_array = self.move_left(board)
            # rotate back to acquire correctly oriented version
            board = np.rot90(board, -movement)
            move_dist = np.rot90(move_dist, -movement)
            merge_array = np.rot90(merge_array, -movement)
            
            if np.array_equal(board, self.board) == False:
                self.board_state_changed = True
                board = self.fill_random_cell(board, self.prime)
                # adds current state to history
                self.history.append(self.board)
                self.move_history.append((move_dist, movement))
                self.merge_history.append(merge_array)
                # overrides current state with new one
                self.board = board
            else:
                self.board_state_changed = False
                
            # update our game status
            self.update_game_status()
            return True
        else:
            print("Error. Please enter one of the following: left, up, right, down. \n \
            Alternatively, type: 0, 1, 2, or 3")
            return False
        
    def get_successor(self, state, action):
        """
        Gets the successor state from performing the specified action
        """
        board = np.copy(state)
        movement = self.get_action(action)
        if movement is None:
            print('Error, retrieved incorrect command')
            return board
        # rotate board to perform left shift movement
        board = np.rot90(board, movement)
        # find desired values from movement operation
        board, move_dist, merge_array = self.move_left(board)
        # rotate back to acquire correctly oriented version
        board = np.rot90(board, -movement)
        return board

    def takeAction(self, action):
        """
        Takes an action and returns the new state we entered
        """
        self.move(action)
        return self.get_current_state()
    
    def check_game_status(self):
        """
        Returns a tuple of (is_game_over?, is_win?)
        """
        return (self.game_over, self.win)

    def update_game_status(self):
        """
        Checks if the game is over. Updates self.game_over and self.win with the correct value.
        
        Outputs:
        --------
        True: game is over
        False : game is ongoing
        """
        loss = True
        for col in range(self.n):
            for row in range(self.m):
                # We won
                #print('Comparing {0} to {1} (goal)'.format(int(self.board[col][row]), self.goal))
                if float(self.board[row][col]) == float(self.goal):
                    #print('reached win condition')
                    self.win = True
                    self.game_over = True
                    return True
                # Checks if the game is still ongoing. If conditions do not hold for all tiles, we lost
                if self.board[row][col] == 0:
                    loss = False
                if (col+1 < self.n) and (self.board[row][col+1] == self.board[row][col]):
                    loss = False
                if (row+1 < self.m) and (self.board[row+1][col] == self.board[row][col]):
                    loss = False

        # If we lost, then game over. If we have not lost nor won, game ongoing.
        if loss == True:
            self.game_over = True
            self.win = False
            return True
        else:
            self.game_over = False
            self.win = False
            return False
        
    def is_win(self):
        """
        Checks if we won the game
        
        Outputs:
        --------
        1: we won
        0: we lost
        """
        for block in np.nditer(self.board):
            if block >= self.goal:
                return True
        return False

    def is_loss(self):
        """
        Checks if we lost the game

        If the left and bottom tiles (if they exist) are equal for any tile, we have not lost yet. If a tile is still empty,
        we have not lost yet.
        """
        for col in range(self.n):
            for row in range(self.m):
                if self.board[row][col] == 0:
                    return False
                if (col+1 < self.n) and (self.board[row][col+1] == self.board[row][col]):
                    return False
                if (row+1 < self.m) and (self.board[row+1][col] == self.board[row][col]):
                    return False
        return True
    
    def get_goal(self):
        """
        Returns our current goal.
        """
        return self.goal

    def get_score(self):
        """
        Gets our current score.
        """
        score = 0
        for tile in np.nditer(self.board):
            score += tile
        return score
    
    def get_val(self, x, y):
        """
        Returns the value of the square at position (x, y)
        """
        return int(self.board[y][x])
    
    def get_all_legal_actions(self):
        """
        Returns a list of all possible actions
        """
        return self.actions

    def get_legal_actions(self, state):
        """
        Returns a list of legal actions at a given state (that actually do something)

        Tries left, up, right, and down movements, and sees which ones actually change
        the board state
        """
        legal_actions = []
        for action in self.main_actions:
            board = self.get_successor(state, action)
            if not np.array_equal(state, board):
                legal_actions.append(action)
        return legal_actions
    
    def get_current_state(self):
        """
        Returns the current board state.
        """
        return self.board
    
    def get_last_state(self):
        """
        Returns the board state we were in before this one, or None of it does not exist.
        """
        if len(self.history) == 0:
            return None
        else:
            return self.history[-1]
        
    def get_last_move_hist(self):
        """
        Returns the distances and direction that tiles in the previous board state moved 
        in order to reach the current state
        """
        if len(self.move_history) == 0:
            return None
        else:
            return self.move_history[-1]
    
    def get_last_fill_coord(self):
        """
        Returns the last coordinate filled by a random number.
        
        fill_coord is a inverse notation (y, x) coordinate
        """
        if len(self.fill_history) == 0:
            return None
        else:
            return self.fill_history[-1]
        
    def get_last_merge_hist(self):
        """
        Returns an array with 1's indicating where the previous state merged tiles while
        moving to the new state. 0 everywhere else.
        """
        if len(self.merge_history) == 0:
            return None
        else:
            return self.merge_history[-1]
        
    def get_board_state_changed(self):
        """
        Returns True if the board state changed with the last move command, False if it didn't
        """
        return self.board_state_changed
    
    def get_filled_last_time(self):
        """
        Returns True if the we filled a random tile with the most recent command, False if we didn't
        """
        return self.filled_last_time
        
    def compute_dest_array(self, prev_state, current_state, move_hist):
        """
        Considers the previous state, the current state, and the move history to compute
        where map all locations in the previous state to locations in the current state
        
        Inputs:
        ------
        prev_state: an array of the previous board state
        current_state: an array of the current board state
        move_hist: a tuple of (move_dist, movement) where move_dist is an array 
                    listing the distance travelled by each tile and movement
                    indicates the direction travelled.
                    (directions mapped as "left" = 0, "up" = 1, "right" = 2, "down" = 3)
                    
        Outputs:
        -------
        dest_array: a destination array mapping each tile in prev_state to its destination 
                    in current_state
                    (uses inverse notation (y, x))
        """
        move_dist, movement = move_hist
        rows, columns = prev_state.shape
        # data type is a list of 64-byte integers [y, x]
        dest_array = np.zeros((rows, columns), dtype='2int64')
        
        for row in range(0, rows):
            for col in range(0, columns):
                shift_x = 0
                shift_y = 0
                
                # left = sub dist in X
                if movement == 0:
                    shift_x = -move_dist[row][col]
                    
                # up = sub dist in Y
                elif movement == 1:
                    shift_y = -move_dist[row][col]
                    
                # right = add dist in X
                elif movement == 2:
                    shift_x = move_dist[row][col]
                    
                # down = add dist in Y
                elif movement == 3:
                    shift_y = move_dist[row][col]
                else:
                    print('Error. Please pass in the correct movement.')
                
                dest_array[row][col] = [row+shift_y, col+shift_x]
                
        return dest_array
    
    def get_dest_array(self):
        """
        Considers the previous state, the current state, and the move history to compute
        where map all locations in the previous state to locations in the current state.
        dest_array uses inverse notation (y, x)
        """
        prev_state = self.get_last_state()
        current_state = self.get_current_state()
        move_hist = self.get_last_move_hist()
        return self.compute_dest_array(prev_state, current_state, move_hist)
        
        
    def undo_last_move(self):
        """
        Reverts the board state to the next most recent state in our history, if it exists
        """
        if len(self.history) != 0:
            last_state = self.history.pop()
            last_move_hist = self.move_history.pop()
            self.board = last_state 