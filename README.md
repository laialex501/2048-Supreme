# 2048-Supreme

Welcome to my personal project! This is an ongoing effort to design and implement a variant of the game "2048" in Python in order to present and demonstrate AI algorithms.

## Game Features

Similarly to regular 2048, this game features a board with numbered tiles. At each timestep, the user is permitted one of four actions: {Left, Up, Right, Down}. 

These actions shift all the numbers on the board in the direction given by the action, with collisions being illegal with one exception: two of the same numbered tile are allowed to merge together when they collide. This merging produces a number of double the size. For example, a collision of 2 and 2 produces 4. When the number 2048 is created, the player wins. 

Unlike regular 2048, this game aspires to allow users more flexibility. Players are permitted to use a board of any size and dimension, not just the 4x4 given in the base game. This also includes non-square shapes like circles, triangles, polygons, etc. 

This game additionally aspires to allow players to use bases other than 2; for example, base 3, which turns the game into "177147" (since 2048 is 2<sup>11</sup>, and 177147 is 3<sup>11</sup>). That said, players are also allowed to define any goal they desire other than the default (so long as it is reachable with their base number!)

## Development Challenges

### Back-End
The requirements above already impose significant design challenges in producing a flexible back-end able to adapt to any of these circumstances.I have been forced to seriously consider the data structures and runtime complexity of my algorithms, given that the board size could theoretically scale to infinity. 

Currently each move of the game runs in *O(n<sup>2</sup>m)* time, where *n* is the number of columns on the board and *m* is the number of rows. While the polynomial time provokes some frowning, believe this to at the very least be close to the optimal solution. 

As a short proof, at minimum we have to consider every tile on the board in the new state, which is *O(nm)* operations. However, given that collisions and merges are expected, we also need to consider how the columns affect one another with each sub-movement. Therefore this is *O(n<sup>2</sup>m)* time. 

### Front-End
In addition to the challenges of the back-end, I have also imposed the requirement of designing and implementing a functional front-end and GUI, including animations for the player to interact with. Given that I have never built a front-end design before, it has been exciting to teach myself how to develop this type of interface. 

Currently I am using the Tkinter graphics library and mimicking the original color scheme of the base 2048 game. 

I also have a healthy appreciation for all the hard work front-end designers do now; I won't laugh when I hear UI design anymore, I promise!

## Ultimate Goal: AI!
Finally, the ultimate goal of this project is to design a custom built environment developed specifically to integrate with various types of AI algorithms, from general tree search (in the deterministic, fully-observable case) to various types of reinforcement learning models. 

I wish to use this platform to demonstrate the various types of AI strategies in a easily presentable and graphical way on a relatively challenging problem (the game "2048" with the various modifications I've made to the rules). 

## In Summary
In summary, the goals of the project are as follows.
- Develop a flexible back-end capable of efficiently handling a board of any size and shape
- Design a robust graphics display on the front-end to clearly communicate the changes to the board state to the player
- Implement AI algorithms using the information acquired from the back-end and present the gathered strategies to the user with the front-end

### List of planned AI strategies: 
- General Tree-Search (Depth First Search, Breadth First Search, Uniform Cost Search/Dijkstra's Algorithm, A* Search using consistent and admissible heuristics)
- Adversarial Search (Minimax, Minimax with Alpha-Beta Pruning, Expectimax)
- Model-Based Reinforcement Learning (Value Iteration, Policy Iteration)
- Model-Free Reinforcement Learning (Q-learning and Approximate Q-learning)
- Constraint Satisfaction algorithms (Backtracking Search with MRV and LCV heuristics, DPLL).
