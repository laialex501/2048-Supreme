import numpy as np
from random import *
import tkinter as tk
import tkinter.messagebox
import time
from Game_World import Game_2048

class StartGame:
    BG = "#fbf8ef"
    ROOT_BASE_WIDTH = 512
    ROOT_BASE_HEIGHT = 512
    TITLE = "2048 Supreme"
    TITLE_TEXT_COLOR = "White"
    SUPREME_COLOR = "#756e64"
    TITLE_HIGHLIGHT_COLOR = "Orange"
    TEXT_COLOR = "#796860"
    TITLE_FONT = ("Helvetica", 28)
    TILE_FONT = ("Helvetica", 16)
    TILE_SIZE = 100
    TILE_SPACING = 15
    TILE_MOVEMENT_SPEED = 0.2
    TILE_OUTLINE = "#b9ab9e"
    TILE_FILL = {0: "#c9bdb1", 2: "#eee4da", 4: "#ece0c8", 8: "#f2b179", 
                   16: "#f29762", 32: "#f57c5f", 64: "#f65d3b" , 128: "#edce71", 
                   256: "#f9d067", 512: "#e4c02a", 1024: "#e4b714", 
                   2048: "#fac42e"}
    TILE_TEXT_COLOR = {0: None, 2: "#796860", 4: "#796860", 8: "white", 16: "white",
                   32: "white", 64: "white", 128: "white", 256: "white", 
                   512: "white", 1024: "white", 2048: "white"}
    TILE_REPO = {}
    ANIMATION_DELAY = .01
    BEGIN_ANIMATION_DELAY = .01
    TILE_PRE_EXPAND_SIZE = 20
    TILE_SCALE_SPEED = 5
    ANIMATION_EXPAND_DELAY = .01
    
    def __init__(self):
        self.GAME = Game_2048()
        # now a constant value
        self.TILE_REPO = {}
        self.finish_animation = True
        
        self.root = tk.Tk()
        self.root.title(self.TITLE)
        # fix root sizing
        self.root.configure(bg=self.BG, width=self.ROOT_BASE_WIDTH, height=self.ROOT_BASE_HEIGHT)

        self.currentFrame = tk.Frame(self.root)
        # should resize after changing into game
        self.enterMainFrame()
        
        self.root.bind_all("<Escape>", self.quit)
        
        self.root.mainloop()

    def setupGenericFrame(self):
        self.root.configure(bg=self.BG, width=self.ROOT_BASE_WIDTH, height=self.ROOT_BASE_HEIGHT)
        genericFrame = tk.Frame(self.root)
        genericFrame.configure(bg=self.BG, width=self.ROOT_BASE_WIDTH, height=self.ROOT_BASE_HEIGHT)
        genericFrame.pack_propagate(True)
        return genericFrame
    
    def setupGameFrame(self):
        self.numRows = self.GAME.m
        self.numCols = self.GAME.n
        self.boardHeight = self.numRows * self.TILE_SIZE + (self.numRows+1) * self.TILE_SPACING
        self.boardWidth = self.numCols * self.TILE_SIZE + (self.numCols+1) * self.TILE_SPACING
        rootWidth = self.boardWidth * 2
        rootHeight = self.boardHeight * 2
        self.root.configure(bg=self.BG, width=rootWidth, height=rootHeight)
        gameFrame = tk.Frame(self.root)
        gameFrame.configure(bg=self.BG, width=rootWidth, height=rootHeight)
        
        return gameFrame

    def enterMainFrame(self):
        self.currentFrame.pack_forget()
        self.currentFrame.destroy()
        mainFrame = self.setupGenericFrame()
        mainFrame.pack_propagate(False)
        mainFrame.pack(fill=tk.BOTH, expand=True)
        self.currentFrame = mainFrame

        mainTitle = tk.Label(mainFrame, text="2048 Supreme", bg=self.TITLE_HIGHLIGHT_COLOR, fg=self.TITLE_TEXT_COLOR, font=self.TITLE_FONT, padx=10, pady=10)
        mainTitle.pack(fill=tk.X, expand=True)

        version = tk.Label(mainFrame, text="v. 1.0", bg=self.BG, fg=self.TEXT_COLOR, font=self.TILE_FONT, padx=5, pady=5)
        version.pack(fill=tk.X, expand=False, side=tk.TOP)

        author = tk.Label(mainFrame, text="by Alex Lai, UC Berkeley", bg=self.BG, fg=self.TEXT_COLOR, font=self.TILE_FONT, padx=5, pady=5)
        author.pack(fill=tk.X, expand=True, side=tk.TOP)

        startNewGame = tk.Button(mainFrame, text="Start New Game", command=lambda: self.enterOptionsFrame(), padx=5, pady=5)
        startNewGame.pack(expand=True)

    def enterOptionsFrame(self):
        self.currentFrame.pack_forget()
        self.currentFrame.destroy()
        optionsFrame = self.setupGenericFrame()
        optionsFrame.pack_propagate(False)
        optionsFrame.pack(fill=tk.BOTH, expand=True)
       	self.currentFrame = optionsFrame

        boardDimensions = tk.Label(optionsFrame, text="Board Dimensions", bg=self.TITLE_HIGHLIGHT_COLOR, fg="White", 
                                   font=self.TILE_FONT, padx=10, pady=10)
        boardDimensions.pack(fill=tk.X, expand=True, side=tk.TOP)

        width = tk.Label(optionsFrame, text="Width", bg="Orange", fg="White", padx=5, pady=5)
        width.pack(expand=True)

        widthOptions = [4, 5, 6, 7, 8, 9, 10]
        widthVar = tk.StringVar(optionsFrame)
        widthVar.set(widthOptions[0])
        widthMenu = tk.OptionMenu(optionsFrame, widthVar, *widthOptions)
        widthMenu.pack(expand=True)

        height = tk.Label(optionsFrame, text="Height", bg=self.BG, fg=self.TEXT_COLOR, padx=5, pady=5)
        height.pack(expand=True)

        heightOptions = [4, 5, 6, 7, 8, 9, 10]
        heightVar = tk.StringVar(optionsFrame)
        heightVar.set(heightOptions[0])
        heightMenu = tk.OptionMenu(optionsFrame, heightVar, *heightOptions)
        heightMenu.pack(expand=True)

        gameOptions = tk.Label(optionsFrame, text="Game Options", bg="Orange", fg="White", 
                               font=self.TILE_FONT, padx=10, pady=10)
        gameOptions.pack(fill=tk.X, expand=1, side=tk.TOP)

        goal = tk.Label(optionsFrame, text="Goal", bg="Orange", fg="White", padx=5, pady=5)
        goal.pack(expand=0)

        goalOptions = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, "Endless"]
        goalVar = tk.StringVar(optionsFrame)
        goalVar.set(2048)
        goalMenu = tk.OptionMenu(optionsFrame, goalVar, *goalOptions)
        goalMenu.pack(expand=True)

        startGameButton = tk.Button(optionsFrame, text="Start Game", 
                                    command=lambda: self.enterGameFrame(widthVar.get(), heightVar.get(), goalVar.get()), 
                                    padx=5, pady=5)
        startGameButton.pack(expand=True)

        returnToMenuButton = tk.Button(optionsFrame, text="Return to Main Menu", command=lambda: self.enterMainFrame(), padx=5, pady=5)
        returnToMenuButton.pack(expand=True)
        
    def enterGameFrame(self, width=4, height=4, goal=2048):
        #print("Width: {0}, Height: {1}, Goal: {2}".format(width, height, goal))
        # remove current frame
        self.currentFrame.pack_forget()
        self.currentFrame.destroy()
        # setup new gameFrame
        self.GAME = Game_2048(m=height, n=width, goal=goal)
        gameFrame = self.setupGameFrame()
        gameFrame.pack()
        self.currentFrame = gameFrame
        
        title=tk.Label(gameFrame, text=self.TITLE, bg=self.BG, fg=self.SUPREME_COLOR, font=self.TITLE_FONT, padx=10, pady=10)
        title.pack()
        
        # Main Board
        boardFrame = tk.Frame(gameFrame, width=self.boardWidth+20, height=self.boardHeight+20, bg=self.BG, padx=10, pady=10)
        boardFrame.pack()
        
        self.canvas = tk.Canvas(boardFrame, width=self.boardWidth, height=self.boardHeight, bg="#baaea0", borderwidth=0)
        self.canvas.pack()
     
        self.init_board()
        
        # Command Frame and Buttons
        commandFrame=tk.Frame(gameFrame, width=self.boardWidth, height=100, bg=self.BG, pady=10, padx=10)
        commandFrame.pack()
        
        self.set_command_buttons(commandFrame)
        
        # Return Button
        returnButton = tk.Button(gameFrame, text="Return to Main Menu", command=lambda: self.enterMainFrame(), padx=5, pady=5)
        returnButton.pack(side=tk.BOTTOM)
        
    def enterEndGameFrame(self, is_game_over, is_win):
    	# remove current frame
        self.currentFrame.pack_forget()
        self.currentFrame.destroy()

        endGameFrame = self.setupGenericFrame()
        endGameFrame.pack_propagate(False)
        endGameFrame.pack()
        self.currentFrame = endGameFrame

        if is_win == True:
        	gameStatusText = "Congrats, you won!"
        else:
        	gameStatusText = "Sorry, you lost."

        gameStatus = tk.Label(endGameFrame, text=gameStatusText, bg=self.TITLE_HIGHLIGHT_COLOR, fg=self.TITLE_TEXT_COLOR, font=self.TITLE_FONT, padx=10, pady=10)
        gameStatus.pack(fill=tk.X, expand=True)

        score_val = self.GAME.get_score()
        scoreText = "Your score was {0}".format(int(score_val))

       	score = tk.Label(endGameFrame, text=scoreText, bg=self.BG, fg=self.TEXT_COLOR, font=self.TILE_FONT, padx=10, pady=10)
       	score.pack(fill=tk.X, expand=True)

       	returnToMenuButton = tk.Button(endGameFrame, text="Return to Main Menu", command=lambda: self.enterMainFrame(), padx=5, pady=5)
        returnToMenuButton.pack(expand=True)
        
    def create_frames(self, root):
        pass
    
    def create_widgets(self):
        pass
    
    def set_command_buttons(self, frame):
        upButton=tk.Button(frame, text="Up", padx=5, pady=5)
        leftButton=tk.Button(frame, text="Left", padx=5, pady=5)
        rightButton=tk.Button(frame, text="Right", padx=5, pady=5)
        downButton=tk.Button(frame, text="Down", padx=5, pady=5)
        
        # primary movement buttons
        upButton.bind("<Button 1>", self.move)
        leftButton.bind("<Button 1>", self.move)
        rightButton.bind("<Button 1>", self.move)
        downButton.bind("<Button 1>", self.move)
        
        upButton.pack(side=tk.TOP)
        leftButton.pack(side=tk.LEFT)
        rightButton.pack(side=tk.RIGHT)
        downButton.pack(side=tk.BOTTOM)
        
        # alternative movement options
        self.root.bind_all("<w>", self.move)
        self.root.bind_all("<a>", self.move)
        self.root.bind_all("<s>", self.move)
        self.root.bind_all("<d>", self.move)
        
        self.root.bind_all("<Up>", self.move)
        self.root.bind_all("<Left>", self.move)
        self.root.bind_all("<Down>", self.move)
        self.root.bind_all("<Right>", self.move)
        
    def move(self, event):
        if event.char == "??":
            command = str(event.widget.cget("text")).lower().strip()
        else:
            command = str(event.keysym).lower().strip()
        if command in self.GAME.get_all_legal_actions():
            if self.finish_animation == True:
                self.GAME.move(command)
                # if the board state changed, then we animate our movement
                if self.GAME.get_board_state_changed():
                    self.finish_animation = self.animate_move()
                    # check if the game is now ever
                    is_game_over, is_win = self.GAME.check_game_status()
                    #print("is_game_over: {0}, is_win: {1}, goal: {2}".format(is_game_over, is_win, self.GAME.goal))
                    if is_game_over:
                        self.enterEndGameFrame(is_game_over, is_win)
                    time.sleep(self.BEGIN_ANIMATION_DELAY)
            else:
                print('Please wait for animation to finish before trying next move.')
        
    def quit(self, event):
        self.root.destroy()
        
    def find_tile_placement(self, col, row):
        """
        Finds the pixel placement of a tile in a given (col, row) or (x, y) location, account for
        TILE_SIZE and TILE_SPACING.
        """
        start_x = self.TILE_SIZE*col + self.TILE_SPACING*(col+1)
        start_y = self.TILE_SIZE*row + self.TILE_SPACING*(row+1)
        end_x = self.TILE_SIZE*(col+1) + self.TILE_SPACING*(col+1)
        end_y = self.TILE_SIZE*(row+1) + self.TILE_SPACING*(row+1)
        
        return start_x, start_y, end_x, end_y
    
    def find_text_placement(self, col, row):
        """
        Finds the pixel placement of the text of a tile in a given (col, row) = (x, y) location,
        accounting for TILE_SIZE and TILE_SPACING. Text is CENTERED at center of tile.
        
        Returns (center_x, center_y) where this is the location where text should be centered at.
        """
        center_x = self.TILE_SIZE*(col+0.5) + self.TILE_SPACING*(col+1)
        center_y = self.TILE_SIZE*(row+0.5) + self.TILE_SPACING*(row+1)
        return center_x, center_y
    
    def create_tile_tk(self, col, row, num):
        """
        Creates a tk shape object at specified (col, row) = (x, y) location in the board with
        the given num. Also creates a tk text object for the given num on the board.
        
        Returns a tuple (tk_shape, tk_text)
        """
        num_bg, num_text_color = self.get_tile_bg_and_text_color(num)
        start_x, start_y, end_x, end_y = self.find_tile_placement(col, row)
        tile = self.canvas.create_rectangle(start_x, start_y, end_x, end_y,
                                                 outline=self.TILE_OUTLINE, fill=num_bg)
    
        if num != 0:
            text_center_x, text_center_y = self.find_text_placement(col, row)
            tile_text = self.canvas.create_text(text_center_x, text_center_y, 
                                                text=str(num), font=self.TILE_FONT, fill=num_text_color)
        else:
            tile_text = None
            
        return (tile, tile_text)
    
    def add_tile_to_repo(self, tile, tile_text, col, row):
        """
        Adds a given tk shape object (tile) and tk text object (tile) and adds it to TILE_REPO as
        a tuple with key (row, col) = (y, x)
        """
        self.TILE_REPO[(row, col)] = (tile, tile_text)
        
    def pop_tile_from_repo(self, col, row):
        """
        Removes the tk shape object mapped to key (row, col) in TILE_REPO and returns it or None 
        if it did not exist
        """
        tile, tile_text = self.TILE_REPO.pop((row, col), None)
        return (tile, tile_text)
        
    def init_board(self):
        """
        Initializes the empty board. Sets up a ZERO tile below every tile. Then finds the initial
        numbers, creates tiles for them, and places them on the board. Also maps the tile objects
        to their (x, y) location on the board in our TILE_REPO object
        """
        # First initialize all tiles to ZERO. These will NEVER be moved.
        for col in range(self.numCols):
            for row in range(self.numRows):
                zero_tile, tile_text = self.create_tile_tk(col, row, 0)
                
        # Now scan array to find all NONZERO tiles, create them, and store them in TILE_REPO. 
        # These WILL be moved at some point in the future.
        for col in range(self.numCols):
            for row in range(self.numRows):
                num = self.GAME.get_val(x=col, y=row)
                if num != 0:
                    init_tile, tile_text = self.create_tile_tk(col, row, num)
                    self.add_tile_to_repo(init_tile, tile_text, col, row)

    def animate_move(self):
        """
        Animates a movement
        """
        self.finish_animation = False
        prev_state = self.GAME.get_last_state()
        dest_arr = self.GAME.get_dest_array()
        fill_coord_y, fill_coord_x = self.GAME.get_last_fill_coord()
        merge_arr = self.GAME.get_last_merge_hist()
        
        numRows, numCols = prev_state.shape
        
        # sets up our tiles to be used for animation
        tiles = []
        # dictionary mapping a (y, x) coord to [list of (tile merging there, 1 if arrived 0 else)]
        merges = {}
        # since we're modifying the original, we iterate over the copy
        TILE_REPO_COPY = self.TILE_REPO.copy()
        for coord, tile_and_text in TILE_REPO_COPY.items():
            # Tile repo uses inverse (y, x) notation
            row, col = coord
            num = self.GAME.get_val(x=col, y=row)
            num_bg, num_text_color = self.get_tile_bg_and_text_color(num)
            dest_y, dest_x = dest_arr[row][col]
            # remove our (tk_tile, tk_tile_text) tuple from REPO for now; if it's still there after animation, we add it back later
            tk_tile, tk_tile_text = self.pop_tile_from_repo(col, row)
            
            #original attempt tries to define movement speed in tiles per second
            animation_tile = self.Tile(start_x=col, start_y=row, 
                                       dest_x=dest_x, dest_y=dest_y, 
                                       background=num_bg, num=num, text_color=num_text_color,
                                       tk_tile = tk_tile, tk_tile_text = tk_tile_text)
            tiles.append(animation_tile)
            
            # 1 if a merge occurs at destination, 0 otherwise
            # merge dict only has 1 object?
            merge = merge_arr[dest_y][dest_x]
            if merge == 1:
                # add list of tiles merging at destination!
                # merges will use inverse notation (y, x)
                if (dest_y, dest_x) in merges:
                    merge_list = merges[(dest_y, dest_x)]
                    merge_list.append(animation_tile)
                    merges[(dest_y, dest_x)] = merge_list
                else:
                    # inits counts of tiles arrived as 0
                    merge_list = [0, animation_tile]
                    merges[(dest_y, dest_x)] = merge_list
            
        while len(tiles) != 0:
            tiles, merges = self.animate_step(tiles, merges)
            time.sleep(self.ANIMATION_DELAY)
            
        # animate fill coord
        # should ONLY fill if fill actually occurred 
        if self.GAME.get_filled_last_time():
            fill_tile, fill_tile_text = self.create_tile_tk(fill_coord_x, fill_coord_y, self.GAME.get_val(x=fill_coord_x, y=fill_coord_y))
            self.add_tile_to_repo(fill_tile, fill_tile_text, fill_coord_x, fill_coord_y)
            # TODO: Get this function to work!
            """self.animate_expand(tile=fill_tile, tile_text=fill_tile_text, 
                                x=fill_coord_x, y=fill_coord_y, min_size=self.TILE_PRE_EXPAND_SIZE, 
                                max_size=self.TILE_SIZE)"""
        
        return True
    
    def animate_step(self, tiles, merge_dict):
        """
        Runs a single step of the animation using the given [tiles] list and merge_dict.
        
        Returns the new [tiles] list after the animation step. Removes tiles from [tiles] 
        if they have reached their destination. 
        
        merge_dict maps a dest coord (x, y) to a merge_list of [count_tiles_arrived, *tiles merging at coord*].
        If the destination is a merge and we have arrived, then increment count_tiles_arrived by 1. If setting 
        this value tells us all merging tiles have arrived (if = len(merge_list)-1), then we proceed with merge.
        So we destroy all the merging tiles and replace with a new tile.

        Note that animate_step ONLY moves colored/non-zero tiles. We already have zero-tiles below everything, 
        so removing the non-zero tile above will reveal the zero-tile below. 
        """      
        # animation step
        new_tiles = []
        for move_tile in tiles: 
            # retrieves movement distance in terms of squares
            # currently movement speed defined in TILES per movement - not PIXELS, which you want
            x_move, y_move = move_tile.move(self.TILE_MOVEMENT_SPEED)

            # convert movement to pixels, accounting for tile spacing
            # NOTE: both the tk_tile and tk_tile_text will move the SAME distance
            x_move = self.TILE_SIZE*x_move + self.TILE_SPACING*(x_move)
            y_move = self.TILE_SIZE*y_move + self.TILE_SPACING*(y_move)     

            tk_tile, tk_tile_text = move_tile.get_tk_obj()
            
            self.canvas.move(tk_tile, x_move, y_move)
            self.canvas.move(tk_tile_text, x_move, y_move)
            #self.canvas.update()

            # if tile not yet at destination, then add back to cycle
            if move_tile.at_dest():
                # if all tiles arrived at merge destination, destroy them and replace with a new tile
                dest = move_tile.get_dest()
                dest_y, dest_x = dest
                
                # our move_tile is part of a merging operation
                # merge_dict uses inverse notation (y, x)
                if dest in merge_dict:
                    # merge_list is a list of [count_tiles_arrived, *tiles*]
                    merge_list = merge_dict[dest]
                    # increment the count of tiles arriving by 1
                    merge_list[0] += 1
                    # indicates all tiles have arrived
                    if merge_list[0] == (len(merge_list) - 1):
                        # delete old tk shapes
                        for merge_tile in merge_list[1:]:
                            tk_tile, tk_tile_text = merge_tile.get_tk_obj()
                            self.canvas.delete(tk_tile)
                            self.canvas.delete(tk_tile_text)
                        #self.canvas.update()
                        # create new tk shape and add to TILE_REPO  
                        num = self.GAME.get_val(x=dest_x, y=dest_y)
                        new_merged_tile, new_merged_tile_text = self.create_tile_tk(col=dest_x, row=dest_y, num=num)
                        # need to add our newly created tile to the repo!
                        self.add_tile_to_repo(tile=new_merged_tile, tile_text=new_merged_tile_text, 
                                              col=dest_x, row=dest_y)
                        # animate the expansion of our tile for visual effect
                        """self.animate_expand(tile=new_merged_tile, tile_text=new_merged_tile_text, 
                                            x=dest_x, y=dest_y, min_size=self.TILE_PRE_EXPAND_SIZE, 
                                            max_size=self.TILE_SIZE)"""
                        # now that the merge is complete, remove the list from the dict
                        merge_dict.pop(dest, None)  
                else:
                    self.add_tile_to_repo(tile=tk_tile, tile_text=tk_tile_text, col=dest_x, row=dest_y)
            # if not at dest then add back to our queue        
            else:
                new_tiles.append(move_tile)
            
        self.canvas.update()
        
        return new_tiles, merge_dict
    
    # TODO: CURRENTLY FUNCTION IS NOT WORKING
    def animate_expand(self, tile, tile_text, x, y, min_size, max_size):
        """
        Animates an expansion of a tile from min_size -> max_size
        
        Expands such that resulting tile position at the board position given by (x, y)
        
        Inputs:
        ------
        tile: the tk tile you wish you perform the animation on
        x: the x position of your tile on the board
        y: the y position of your tile on the board
        min_size: the length of one side of your minimum tile
        max_size: the length of one side of your maximum tile
        """
        norm_start_x, norm_start_y, norm_end_x, norm_end_y = self.find_tile_placement(x, y)
        dist_max = (max_size - self.TILE_SIZE)/2
        top_left_x = norm_start_x - dist_max
        top_left_y = norm_start_y - dist_max
        bottom_right_x = norm_end_x + dist_max
        bottom_right_y = norm_end_y + dist_max
        
        # move forward to min, move backward to max
        dist_min = (max_size - min_size)/2
        x_start = top_left_x + dist_min
        y_start = top_left_x + dist_min
        x_end = x_start + min_size
        y_end = y_start + min_size
        self.canvas.coords(tile, x_start, y_start, x_end, y_end)
        
        while (x_start != top_left_x) and (y_start != top_left_y):
            x_start -= min(self.TILE_SCALE_SPEED, x_start - top_left_x)
            y_start -= min(self.TILE_SCALE_SPEED, y_start - top_left_y)
            x_end += min(self.TILE_SCALE_SPEED, bottom_right_x - x_end)
            y_end += min(self.TILE_SCALE_SPEED, bottom_right_y - y_end)
            self.canvas.coords(tile, x_start, y_start, x_end, y_end)
            time.sleep(self.ANIMATION_EXPAND_DELAY)
        return True
                
    def get_tile_bg_and_text_color(self, num):
        """
        Takes in a number and returns the corresponding background and text_color
        """
        if num in self.TILE_FILL:
            num_bg = self.TILE_FILL[num]
            num_text_color = self.TILE_TEXT_COLOR[num]
        else:
            num_bg = self.TILE_FILL[2048]
            num_text_color = self.TILE_TEXT_COLOR[2048]
            
        return (num_bg, num_text_color)
        
        
    class Tile:
        """
        Objects to be used for animation of tiles
        """
        def __init__(self, start_x, start_y, dest_x, dest_y, background, num, text_color, tk_tile, tk_tile_text):
            self.current_x = start_x
            self.current_y = start_y
            self.dest_x = dest_x
            self.dest_y = dest_y
            self.bg = background
            self.num = num
            self.text_color = text_color
            self.tk_tile = tk_tile
            self.tk_tile_text = tk_tile_text
            
        def get_tk_obj(self):
            """
            Returns a tuple of our tk objects (tk_tile, tk_tile_text)
            """
            return (self.tk_tile, self.tk_tile_text)
        
        def get_dest(self):
            """
            Returns the destination of our tile as a tuple in reverse notation (dest_y, dest_x)
            """
            return (self.dest_y, self.dest_x)
        
        def move(self, movement_speed):
            """
            Moves the object from our (current_x, current_y) -> (dest_x, dest_y) in a straight line.
            
            Updates our current position and returns the amount we moved. If we would overshoot then 
            moves only as far as necessary.
            """
            
            x_dist = self.dest_x - self.current_x
            y_dist = self.dest_y - self.current_y
            
            x_dir = np.sign(x_dist)
            y_dir = np.sign(y_dist)

            # if we would overshoot the distance with the movement, just take the distance as the movement
            # factors: if x_dist is ZERO, or x_dist < movement speed, then we only move just enough
            # x movement determined by sign of x_dist
            x_movement = x_dir * min(abs(x_dist), movement_speed)
            y_movement = y_dir * min(abs(y_dist), movement_speed)
            
            new_x = self.current_x + x_movement
            new_y = self.current_y + y_movement
            
            self.current_x = new_x
            self.current_y = new_y
            
            return (x_movement, y_movement)
            
        def at_dest(self):
            """
            Returns true if we've reached our goal. False otherwise.
            """
            if self.current_x == self.dest_x and self.current_y == self.dest_y:
                return True
            else:
                return False
            
        def __str__(self):
            return "current_x: {0}, current_y: {1}, dest_x: {2}, dest_y: {3}".format(self.current_x, self.current_y, 
                                                                                      self.dest_x, self.dest_y)
        
        def __eq__(self, other): 
            try:
                return self.tk_tile == other.tk_tile
            except AttributeError:
                print('Exception occured')
                return False