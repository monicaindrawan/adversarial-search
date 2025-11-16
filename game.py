


class ManualPlayer:
    def __init__(self):
        pass
    
    def select_cell(self, m, n):
        while True:
            print("Choose a square to Play")
            try:
                cell_coordinate = input().split(' ')
                x, y = int(cell_coordinate[0]), int(cell_coordinate[1])
                if x > m or y > n or x < 1 or y < 1:
                    print("Input Out of Range")
                    continue
                else:
                    return (x, y)
            except KeyboardInterrupt:
                exit()
            except:
                print("Invalid Input Format, Input Format is 'x y'")
                

class AutomaticPlayer:
    def __init__(self):
        pass
        

class Game:
    def __init__(self, m: int, n: int, k: int):
        self.initialize_game(m, n, k)
        
        
    def initialize_game(self, m: int, n: int, k: int, starting_player: int = 1):
        self.m = m
        self.n = n
        self.k = k
        
        self.cells1 = set()
        self.cells2 = set()
        
        self.player1 = ManualPlayer()
        self.player2 = AutomaticPlayer()
        
        self.current_player = starting_player    # 0 for Max (the actual player), 1 for Min (the automatic player)
            
    
        
    def play(self):
        while self.has_ended() == False:
            self.turn()
        
    
    def turn(self):
        if self.current_player == 1:
            print("Player 1 Turn")
            while True:
                x, y = self.player1.select_cell(self.m, self.n)
                if (x, y) not in self.cells1 and (x, y) not in self.cells2:
                    self.cells1.add((x, y))
                    # self.current_player = 2
                    break
                else:
                    print("Cell already taken")
                    continue
        
        elif self.current_player == 2:
            pass
        
        self.print_board()
        
    def has_ended(self):
        return False
    

    def print_board(self):
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