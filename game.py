import time

class Game:
    """
    A class implementing a generalised mnk game, on a m-by-n board game where k consecutive 
    marks are required to win.
    
    The game includes an AI implementation using the Minimax algorithm with 
    Alpha-Beta pruning.
    
    Attributes:
        m (int): Number of columns (width).
        n (int): Number of rows (height).
        k (int): Number of consecutive marks needed to win.
        cells1 (set): Set of coordinate tuples (x, y) occupied by Player 1.
        cells2 (set): Set of coordinate tuples (x, y) occupied by Player 2.
        empty_cells (set): Set of available coordinate tuples.
        current_player (int): ID of the player whose turn it is (1 or 2).
    """
    
    def __init__(self, m: int, n: int, k: int):
        """
        Initialises the game instance.

        Args:
            m (int): Number of columns.
            n (int): Number of rows.
            k (int): Win condition length.
        """
        self.initialize_game(m, n, k)

    def __str__(self):
        return f"Game of m: {self.m}, n: {self.n}, k: {self.k}"
        
        
    def initialize_game(self, m: int, n: int, k: int):
        """
        Resets the game state, clears the board, and sets the starting player.
        """
        self.m = m
        self.n = n
        self.k = k
        
        # Using sets for O(1) lookup time when checking if a cell is occupied
        self.cells1 = set()
        self.cells2 = set()
        
        # last placed cells are used to quickly check the game state (whether one player has won)
        self.last_placed_cell1 = None
        self.last_placed_cell2 = None
        
        # Generate all possible coordinates for the board, empty_cells is used for quick look up for possible next moves by minimax
        self.empty_cells = set()
        for x in range(1, m+1):
            for y in range(1, n+1):
                self.empty_cells.add((x, y))

        self.current_player = 1                 # 1 for Max (the actual player), 2 for Min (the automatic player)
        self.visited_states_count = 0           # tracks number of states visited across each move
    
        
    def play(self):
        """
        Main game loop. Continues until a win, loss, or draw occurs.
        """
        while True:
            # play the turn
            self.turn()
            
            # check whether the game has won by either player or is a draw
            board_state = self.check_state()
            if board_state == 1:
                print("Player 1 Won!")
                return
            elif board_state == 2:
                print("Player 2 Won!")
                return
            elif board_state == 0 and len(self.empty_cells) == 0:
                print("Draw!")
                return
            
            # swap the current player to the other
            self.swap_turn()
        
    
    def turn(self, draw=True):
        """
        Executes the logic for a single turn.
        
        Player 1 is the Human player (with AI hints provided).
        Player 2 is the AI player (moves automatically).
        """
        x, y = (-1, -1)
        # Player 1 (user) turn
        if self.current_player == 1:
            print("Player 1 Turn")
            
            self.visited_states_count = -1
            start_time = time.time()
            # Calculate the best move using minimax with alpha beta pruning
            value, move = self.max_value(float('-inf'), float('inf'))
            end_time = time.time()
    
            print(f"Recommended Move {move[0]} {move[1]}")
            
            # Input loop: ensure user picks a valid, empty cell
            while True:
                x, y = self.select_cell()
                if (x, y) not in self.cells1 and (x, y) not in self.cells2:
                    self.cells1.add((x, y))
                    self.empty_cells.remove((x, y))
                    self.last_placed_cell1 = (x, y)
                    break
                else:
                    print("Cell already taken")
                    continue
        # Player 2 (AI) turn
        elif self.current_player == 2:
            print("Player 2 Turn")

            self.visited_states_count = -1
            start_time = time.time()
            # AI calculates the best move for itself (Minimising strategy)
            value, move = self.min_value(float('-inf'), float('inf'))
            end_time = time.time()
            
            # AI plays the move directly calculated above
            self.cells2.add(move)
            self.empty_cells.remove(move)
            self.last_placed_cell2 = move
            
        if draw:
            self.drawboard()


    def swap_turn(self):
        """Toggles the current player between 1 and 2."""
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        
    def max_value(self, alpha, beta):
        """
        Minimax function for the Maximizing player (Player 1).
        
        Args:
            alpha (float): The best value that the maximiser currently can guarantee.
            beta (float): The best value that the minimiser currently can guarantee.
            
        Returns:
            tuple: (Best Score, Best Move Coordinate)
        """
        # Add to visited counter
        self.visited_states_count += 1
        # check if any player has won
        board_state = self.check_state()
        
        best_value = float("-inf")
        best_move = None
        original_cell = self.last_placed_cell1
        
        # if at the end state, player 1 wins, return 1, if player 2 wins return 2
        if board_state == 1:
            return (1, None)
        elif board_state == 2:
            return (-1, None)
        # if there are no possible moves left, return 0 for draw
        if len(self.empty_cells) == 0:
            return (0, None)

        elif board_state == 0:
            # Iterate through possible moves (ordered for better pruning)
            for move in self.get_ordered_moves():
                # add the move to the player 1 cells
                self.cells1.add(move)
                self.empty_cells.remove(move)
                self.last_placed_cell1 = move
                # Call min node (opponent's turn)
                new_value = self.min_value(alpha, beta)[0]
                
                # Get the maximum value of the child nodes, set the best move to the maximum value achieved
                if best_value < new_value:
                    best_value = new_value
                    best_move = move
                # Backtrack to undo the exploration moves from the board
                self.cells1.remove(move)
                self.empty_cells.add(move)
                
                # Alpha-Beta Pruning
                # Prune if current best value is greater than beta
                if best_value >= beta:
                    self.last_placed_cell1 = original_cell
                    return best_value, best_move

                # Update alpha based on current best value
                alpha = max(alpha, best_value)
                
        # revert the last placed cell to the beginning of the function
        self.last_placed_cell1 = original_cell
        return best_value, best_move
    
    
    def min_value(self, alpha, beta):
        # same logic here as max_value
        self.visited_states_count += 1
        board_state = self.check_state()
        
        best_value = float("inf")
        best_move = None
        original_cell = self.last_placed_cell2
        
        if board_state == 1:
            return (1, None)
        elif board_state == 2:
            return (-1, None)
        if len(self.empty_cells) == 0:
            return (0, None)

        elif board_state == 0:
            for move in self.get_ordered_moves():
                self.cells2.add(move)
                self.empty_cells.remove(move)
                self.last_placed_cell2 = move
                
                # Call Max node (opponent's turn)
                new_value = self.max_value(alpha, beta)[0]
                
                # Find the minimum value and best move according to that
                if best_value > new_value:
                    best_value = new_value
                    best_move = move
                self.cells2.remove(move)
                self.empty_cells.add(move)

                # Alpha-Beta Pruning
                # Prune if current best value is smaller than alpha
                if best_value <= alpha:
                    self.last_placed_cell2 = original_cell
                    return best_value, best_move
                
                # Update beta based on current best value
                beta = min(beta, best_value)
            
        self.last_placed_cell2 = original_cell
        return best_value, best_move


    def get_ordered_moves(self):
        """
        Heuristic to sort empty cells based on distance to the board center.
        
        Alpha-beta pruning works best when the best moves are explored first so more subtrees can be pruned.
        Assume squares towards the center are better moves in general
        """
        center = (self.m / 2, self.n / 2)
        return sorted(list(self.empty_cells), key=lambda p: (p[0]-center[0])**2 + (p[1]-center[1])**2)
    
    
    def check_state(self):
        """
        Determines the current state of the game.
        
        Returns:
            int: 1 if Player 1 won, 2 if Player 2 won, 0 if game continues or draw.
        """
        player1_won = self.check_terminal(self.cells1, self.last_placed_cell1)
        if player1_won == True:
            return 1
        
        player2_won = self.check_terminal(self.cells2, self.last_placed_cell2)
        if player2_won == True:
            return 2
        
        return 0
    
    
    def check_terminal(self, cells, last_placed_cell=None):
        """
        Check if the game has ended

        Args:
            cells (set of tuple) : current taken cells by player
            last_placed_cell (tuple) : current picked cell by player

        Returns:
            bool : True if game has ended, False if it has not
        """

        if last_placed_cell == None:
            return False

        # Initiliaze checking directions
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for direction in directions:
            count = 1

            # Looping two sides of each direction
            for dir in ['+', '-']:
                current_cell = last_placed_cell
                while True:
                    # Generate neighbour cell
                    if dir == '+':
                        current_cell = (current_cell[0] + direction[0], current_cell[1] + direction[1])
                    else:
                        current_cell = (current_cell[0] - direction[0], current_cell[1] - direction[1])

                    if self.is_valid(current_cell):
                        
                        if current_cell in cells:
                            # Track cells if neighbour cell is taken by player
                            count += 1
                        else:
                            break
                    else:
                        break
                
            # Return True if the consequtive picked cells have reached length of k
            if count >= self.k:
                return True
        return False

    
    def is_valid(self, coordinate):
        """
        Check if a cell is within board

        Args:
            coordinate (tuple) : current observed neighbouring cell
    
        Returns:
            bool : True if neighbouring cell is within board
        """
        
        x = coordinate[0]
        y = coordinate[1]

        # Check if x and y is within bounds
        if x > self.m or y > self.n or x < 1 or y < 1:
            return False
         
        return True
    
        
    def select_cell(self):
        """Handles player input for coordinates."""
        # Keep asking the player to choose coordinate, until the chosen coordinate is valid
        while True:
            print("Choose a square to Play")
            # check for valid coordinate
            try:
                cell_coordinate = input().split()
                x, y = int(cell_coordinate[0]), int(cell_coordinate[1])
                if x > self.m or y > self.n or x < 1 or y < 1:
                    print("Input Out of Range")
                    continue
                else:
                    return (x, y)
            # if the user enter control-c, let them exit
            except KeyboardInterrupt:
                exit()
            except:
                print("Invalid Input Format, Input Format is 'x y'")
    

    def drawboard(self):
        board_str = ""
        
        # draws header for x coordinate labels
        board_str += "   "
        for x in range(1, self.m+1):
            board_str += f"{x} "
        board_str += "\n\n"
        
        for y in range(1, self.n+1):
            # draws y coordinate labels
            board_str += f"{y}  "
            for x in range(1, self.m+1):
                # draws the board values at each (x, y), 1 for player 1, 2 for player 2, 0 for empty
                if (x, y) in self.cells1:
                    board_str += '1'
                elif (x, y) in self.cells2:
                    board_str += '2'
                else:
                    board_str += '0'
                board_str += ' '
            board_str += '\n'
        
        print("")
        print("Current Board:")
        print(board_str)
    
    
    
def get_input_config():
    """Prompts user for game configuration (rows, columns, win length)."""
    # similar logic to select_cell above
    while True:
        print("Enter game config (m n k), e.g. '3 3 3'")
        try:
            input_list = input().split()
            m, n, k = int(input_list[0]), int(input_list[1]), int(input_list[2])
            if k > m and k > n:
                print("Please enter valid k values")
            else:
                print('')
                return (m, n, k)
        except KeyboardInterrupt:
            exit()
        except:
            print("Please enter valid (m n k) values")
        
    
# Main entry point
if __name__ == "__main__":
    m, n, k = get_input_config()
    
    game = Game(m, n, k)
    game.play()