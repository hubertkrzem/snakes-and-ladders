import random as r

'''
1. Build a representation of a the s&l board with regular squares, snakes and ladders.
2. Create board square interpreter, if square == (reg, snk, ldr): change pos accordingly.
3.

--- Class ---
Pawn:
- Holds postion
- Takes in position updates,
    - Dice roll update (pos + 2)
    - Complete update (Hit ladder pos = ladder end)

Board:
- Track all squares (empty, snake, ladder)
- Track snake ladder mapping


--- Controller ---
- Generate board
- Generate pawn(s)
- Run dicerolls
- Update pawn positions depending on
'''

def snakesAndLadders():

    class Pawn():
        def __init__(self):
            self.pos = 0

        def updatePos(self, newPos):
            self.pos = newPos

        def movePos(self, moves):
            self.pos += moves

    # Function for menu and taking inputs
    def menu():
        while True:
            welcome = (
                f"\n"
                f"{"="*50}\n"
                f"{"Snakes and Ladders Monte Carlo Simulaton":^50}\n"
                f"{" "*50}\n"
                f"© 2026 Hubert Krzemieniewski. All rights reserved.\n"
                f"{"="*52}"
                f"\n"
            )

            choiceMessage = (
                f"Select mode (1-3):\n"
                f"1. Single simulation\n"
                f"2. Monte Carlo Simulation\n"
                f"3. Exit\n"
                f"> "
            )
                
            print(welcome)
            choice = "1" # input(choiceMessage)

            if choice == "1":   # Single Simulation
                controller()
                print(input())          
      
            elif choice == "2": # Monte Carlo Simulation
                print("\nFeature not ready")
            elif choice == "3": # Exit
                print("\nThanks for using my program :)")
                break
            else:
                print("\nInvalid choice. Please try again.")

    # Function for generating game board
    def boardGenerator(length=100, snakes=10, ladders=10):
        # Generate board
        board = list(range(length))

        modifiers = {}

        # Generate snakes
        snakeStarts = r.sample(range(1, length-1), snakes)              # Set snakeStarts as random values from 0 to board length-1 (if snake on last cell pawn cant finish)
        snakeEnds = [r.randint(0, start-1) for start in snakeStarts]    # Set snakeEnds as random values from 0 to corresponding snakeStart -1 (snake dosent move player forward, moves atleast one cell back)
        snakeMap = {}

        i = 0
        for start in snakeStarts:
            snakeMap[start] = snakeEnds[i]
            modifiers[start] = snakeEnds[i]
            i += 1

        # Generate Ladders
        ladderStarts = r.sample(range(0, length-1), ladders)                # Set ladderStarts as random values from 0 to board length-1 (if ladder starts on last cell, no cell is ahead)
        ladderEnds = [r.randint(start+1, length) for start in ladderStarts] # Set ladderEnds as random values from corresponding ladderStart+1 to end (ladder dosent move player back, moves atleast one cell forward)
        ladderMap = {}

        i = 0
        for start in ladderStarts:
            ladderMap[start] = ladderEnds[i]
            modifiers[start] = snakeEnds[i]
            i += 1

        # return snakeMap, ladderMap
        return board, modifiers
 
    # Function for running the game and returning results
    def controller():
        # Returns random number in range, simulating diceroll
        def diceRoll(sides=6):
            return r.randint(1, 6)
        

        board, modifiers = boardGenerator()
        print(board)
        # print(f"Snakes: {snakeMap}")
        # print(f"Ladders: {ladderMap}")
        print(f"All modifiers: {modifiers}")

    menu()

if __name__ == "__main__":
    snakesAndLadders()
    
