

class Game:
    def __init__(self, m: int, n: int, k: int):
        self.initialize_game(m, n, k)
        
        
        
    def initialize_game(self, m: int, n: int, k: int, starting_player: int = 1):
        self.m = m
        self.n = n
        self.k = k
        
        self.cells1 = set()
        self.cells2 = set()
        
        self.empty_cells = set()
        for x in range(m):
            for y in range(n):
                self.empty_cells.add((x, y))

        self.current_player = starting_player    # 0 for Max (the actual player), 1 for Min (the automatic player)
        self.last_placed_cell = None
    
        
    def play(self, auto = False):
        while True:
            self.turn()
            print(self.is_terminal())
            
            if self.is_terminal():
                return False
    
    
    def turn(self, draw = True):
        x, y = (-1, -1)
        if self.current_player == 1:
            print("Player 1 Turn")
            while True:
                x, y = self.select_cell()
                print(x,y)
                if (x, y) not in self.cells1 and (x, y) not in self.cells2:
                    self.cells1.add((x, y))
                    # self.current_player = 2
                    break
                else:
                    print("Cell already taken")
                    continue
            
        elif self.current_player == 2:
            pass
        
        self.last_placed_cell = (x, y)
        self.drawboard()

        
        
    def max_value(self):
        board_state = self.check_state()
        
        best_value = float("-inf")
        best_move = (-1, -1)
        
        if board_state == 1:
            return (1, None)
        elif board_state == 2:
            return (-1, None)
        elif board_state == 0:
            for move in self.possible_moves(self.cells1, self.cells2):
                self.cells1.add(move)
                new_value = self.min_value(self.cells1, self.cells2)[0]
                if best_value < new_value:
                    best_value = new_value
                    best_move = move
                self.cells1.remove(move)
            
        return best_value, best_move
    
    
    def min_value(self):
        board_state = self.check_state()
        
        best_value = float("inf")
        best_move = (-1, -1)
        
        if board_state == 1:
            return (1, None)
        elif board_state == 2:
            return (-1, None)
        elif board_state == 0:
            for move in self.possible_moves(self.cells1, self.cells2):
                self.cells2.add(move)
                new_value = self.max_value(self.cells1, self.cells2)[0]
                if best_value > new_value:
                    best_value = new_value
                    best_move = move
                self.cells2.remove(move)
        
        return best_value, best_move
    
    
        
    def is_terminal(self):
        if self.current_player == 1:
            attacked_cells = self.cells1
        else:
            attacked_cells = self.cells2
        
        return self.check_terminal(attacked_cells)
    
    
    def check_state(self):
        player1_won = self.check_terminal(self.cells1)
        if player1_won:
            return 1
        player2_won = self.check_terminal(self.cells2)
        if player2_won:
            return -1
        
        return 0
    
    
    def check_terminal(self, cells):
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for direction in directions:
            count = 1

            for dir in ['+', '-']:
                current_cell = self.last_placed_cell
                while True:
                    if dir == '+':
                        current_cell = (current_cell[0] + direction[0], current_cell[1] + direction[1])
                    else:
                        current_cell = (current_cell[0] - direction[0], current_cell[1] - direction[1])

                    if self.is_valid(current_cell):
                        if current_cell in cells:
                            count += 1
                        else:
                            break
                    else:
                        break
        
            if self.k == count:
                return True
        return False

    
    def is_valid(self, coordinate):
        x = coordinate[0]
        y = coordinate[1]

        if x > self.m or y > self.n or x < 1 or y < 1:
            return False
         
        return True
    
    def player1_move(self, coordinate):
        x, y = coordinate
        self.cells1.add((x, y))
        self.empty_cells.remove((x, y))
        
    def player2_move(self, coordinate):
        x, y = coordinate
        self.cells2.add((x, y))
        self.empty_cells.remove((x, y))
        
        
    def select_cell(self):
        while True:
            print("Choose a square to Play")
            try:
                cell_coordinate = input().split(' ')
                x, y = int(cell_coordinate[0]), int(cell_coordinate[1])
                if x > self.m or y > self.n or x < 1 or y < 1:
                    print("Input Out of Range")
                    continue
                else:
                    return (x, y)
            except KeyboardInterrupt:
                exit()
            except:
                print("Invalid Input Format, Input Format is 'x y'")
    

    def drawboard(self):
        board_str = ""
        for y in range(1, self.n+1):
            for x in range(1, self.m+1):
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
    
    
    
if __name__ == "__main__":
    game = Game(3, 3, 3)
    game.play()