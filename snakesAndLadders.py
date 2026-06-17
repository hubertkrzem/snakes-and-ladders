import random as r

'''
1. Build a representation of a the s&l board with regular squares, snakes and ladders.
2. Create board square interpreter, if square == (reg, snk, ldr): change pos accordingly.
3.

--- Objects ---
Pawn:
- Holds postion
- Takes in position updates,
    - Dice roll update (pos + 2)
    - Complete update (Hit ladder pos = ladder end)

--- Controller ---
- Generate board
- Generate pawn(s)
- Run dicerolls
- Update pawn positions
- Detects win condition
'''

class Pawn():
    def __init__(self, name):
        self.pos = 0
        self.name = name

    def __repr__(self): # if type(self.name) == int(): return f"Pawn {self.name}" else:
        return f"{self.name}"
    
    def __str__(self):
        return f"{self.name}"
    
    def addMove(self, moves):
        self.pos += moves

    def setPos(self, newPos):
        self.pos = newPos

    def getPos(self):
        return self.pos


def boardGenerator(length=100, snakes=10, ladders=10):
    board = list(range(length))
    modifiers = {}

    # Generate snakes
    snakeStarts = r.sample(range(1, length-1), snakes)              # Set snakeStarts as random values from 0 to board length-1 (if snake on last cell pawn cant finish)
    snakeEnds = [r.randint(0, start-1) for start in snakeStarts]    # Set snakeEnds as random values from 0 to corresponding snakeStart -1 (snake dosent move player forward, moves atleast one cell back)
    snakeMap = {}

    # Generate Ladders
    ladderStarts = r.sample(range(0, length-1), ladders)                # Set ladderStarts as random values from 0 to board length-1 (if ladder starts on last cell, no cell is ahead)
    ladderEnds = [r.randint(start+1, length) for start in ladderStarts] # Set ladderEnds as random values from corresponding ladderStart+1 to end (ladder dosent move player back, moves atleast one cell forward)
    ladderMap = {}

    i = 0
    for start in ladderStarts:
        snakeMap[start] = snakeEnds[i]
        modifiers[start] = snakeEnds[i]

        ladderMap[start] = ladderEnds[i]
        modifiers[start] = ladderEnds[i]
        i += 1

    return modifiers, snakeMap, ladderMap

def controller(boardLength=100, snakes=10, ladders=10, pawnNum=1):
    # Game generation
    pawnNum = int(pawnNum)
    pawns = [Pawn(f"P{i}") for i in range(0, pawnNum)]
    modifiers, snakeMap, ladderMap = boardGenerator(boardLength, snakes, ladders)

    # Game running
    liveGame = True
    while liveGame:
        for pawn in pawns:
            roll = diceRoll()
            currPos = pawn.getPos()

            print(f"{pawn} rolls {roll}")
            print(f"Current position: {currPos}")
            print(f"New position: {currPos + roll}")
            
            # --- Move validation ---
            # Move not > board length
            if (currPos + roll) > boardLength:
                print(f"Roll too high, move invalid\n")
                continue
            else:
                pawn.addMove(roll)
                
                if pawn.getPos() in modifiers:
                    prev = pawn.getPos()
                    pawn.setPos(modifiers[prev])
                    new = pawn.getPos()

                    if prev > new:
                        print(f"{pawn} hit a snake and fell from {prev} to {new}")
                    elif new > prev:
                        print(f"{pawn} hit a ladder and climbed from {prev} to {new}")
            print()
            if pawn.getPos() == boardLength:
                print(f"***** {pawn} has won the game *****\n")
                liveGame = False
                break
    
    # Snake & Ladders map output
    print(f"Snakes: {snakeMap}")
    print(f"Ladders: {ladderMap}")
    # print(f"All modifiers: {modifiers}")

def diceRoll(sides=6):
    return r.randint(1, 6)

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
        choice = input(choiceMessage)

        if choice == "1":   # Single Simulation
            controller(pawnNum=input(f"Number of pawns:\n> "))
            print(input())          
    
        elif choice == "2": # Monte Carlo Simulation
            print("\nFeature not ready")

        elif choice == "3": # Exit
            print("\nThanks for using my program :)")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    menu()
    
