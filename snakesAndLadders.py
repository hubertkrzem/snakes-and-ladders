import random
from dataclasses import dataclass

'''
1. Build a representation of a the s&l board with regular squares, snakes and ladders.
2. Create board square interpreter, if square == (reg, snk, ldr): change pos accordingly.

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

3. Full extent of game customisation

4. Stat tracking for monte carlo simulations
--- Statistics ---
- # of moves per game
- snake hits
- ladder hits
- squares heatmap
- 

5. Manual single player mode
'''

class Pawn():
    def __init__(self, name):
        self.pos = 0
        self.name = name

    def __repr__(self):
        return f"{self.name}"
    
    def __str__(self):
        return f"{self.name}"
    
@dataclass
class GameStats:
    moves: int = 0
    snakeHits: int = 0
    ladderHits: int = 0
    
def boardGenerator(length=100, snakes=10, ladders=10) -> tuple[dict, dict, dict]:
    modifierMap = {}

    # Generate snakes
    snakeStarts = random.sample(range(1, length-1), snakes)              # Set snakeStarts as random values from 0 to board length-1 (if snake on last cell pawn cant finish)
    snakeEnds = [random.randint(0, start-1) for start in snakeStarts]    # Set snakeEnds as random values from 0 to corresponding snakeStart -1 (snake dosent move player forward, moves atleast one cell back)
    snakeMap = {}

    for i, start in enumerate(snakeStarts):
        snakeMap[start] = snakeEnds[i]
        modifierMap[start] = snakeEnds[i]

    # Generate Ladders
    ladderStarts = random.sample(range(0, length-1), ladders)                # Set ladderStarts as random values from 0 to board length-1 (if ladder starts on last cell, no cell is ahead)
    ladderEnds = [random.randint(start+1, length) for start in ladderStarts] # Set ladderEnds as random values from corresponding ladderStart+1 to end (ladder dosent move player back, moves atleast one cell forward)
    ladderMap = {}

    for i, start in enumerate(ladderStarts):
        ladderMap[start] = ladderEnds[i]
        modifierMap[start] = ladderEnds[i]

    return modifierMap, snakeMap, ladderMap

def controller(boardLength=100, snakes=10, ladders=10, pawnNum=2, gamesNum=1, verbose=True):
    pawns, modifierMap, snakeMap, ladderMap = buildGame(pawnNum, boardLength, snakes, ladders)

    runGame(pawns, modifierMap, gamesNum, boardLength, verbose)

    # Snake & Ladders map output
    print(f"Snakes: {snakeMap}")
    print(f"Ladders: {ladderMap}\n")

def buildGame(pawnCount, boardLength, snakes, ladders):
    pawns = [Pawn(f"P{i}") for i in range(pawnCount)]
    modifierMap, snakeMap, ladderMap = boardGenerator(boardLength, snakes, ladders)

    return pawns, modifierMap, snakeMap, ladderMap

def runGame(pawns, modifierMap, numGames, boardLength, verbose):
    runStats = GameStats()

    for _ in range(numGames):
        gameStats = GameStats()

        gameActive = True
        while gameActive:
            for pawn in pawns:
                roll = diceRoll()
                gameStats.moves += 1
                currentPos = pawn.pos

                if verbose:
                    print(f"{pawn} rolls {roll}")
                    print(f"Current position: {currentPos}")
                    print(f"New position: {currentPos + roll}")

                # --- Move validation ---
                # Move not > board length
                if (currentPos + roll) > boardLength:
                    if verbose:
                        print(f"Roll too high, move invalid")
                    continue
                else:
                    pawn.pos += roll

                    if pawn.pos in modifierMap:
                        squareLanded = pawn.pos
                        pawn.pos = modifierMap[squareLanded]
                        squareFinal = pawn.pos

                        if squareLanded > squareFinal:
                            gameStats.snakeHits += 1
                            if verbose:
                                print(f"{pawn} hit a snake and fell from {squareLanded} to {squareFinal}")
                        elif squareFinal > squareLanded:
                            gameStats.ladderHits += 1
                            if verbose:
                                print(f"{pawn} hit a ladder and climbed from {squareLanded} to {squareFinal}")
        
                if pawn.pos == boardLength:
                    # if verbose:
                    print(f"\n***** {pawn} has won the game *****")
                    print(f"Total moves: {gameStats.moves}")
                    
                    # --- Update stats ---
                    runStats.moves += gameStats.moves
                    runStats.snakeHits += gameStats.snakeHits
                    runStats.ladderHits += gameStats.ladderHits

                    gameActive = False
                    break

        # --- Simulation reset ---
        for pawn in pawns:
            pawn.pos = 0

    print(statSummary(numGames, runStats))

def statSummary(numGames, gamesStats):
    output = (
        f"\nStats over {numGames:,} game{'s' if numGames != 1 else ''}\n"
        f"{"Total moves:":<22} {gamesStats.moves}\n"
        f"{"Moves per game:":<22} {gamesStats.moves/numGames:.1f}\n"
        f"{"Snake hits per game:":<22} {gamesStats.snakeHits/numGames:.1f}\n"
        f"{"Ladder hits per game:":<22} {gamesStats.ladderHits/numGames:.1f}\n"
        f"{"Total Snake hits:":<22} {gamesStats.snakeHits}\n"
        f"{"Total Ladder hits:":<22} {gamesStats.ladderHits}\n"
    )

    return output

def diceRoll(sides=6) -> int:
    return random.randint(1, sides)

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

        # --- Single Simulation setup ---
        if choice == "1":
            print("Single Simulation")
            while True:
                default = input("Default settings (y/n):\n> ").capitalize()
                
                if default == "Y":
                    controller()
                    break

                elif default == "N":
                    lengthIn=int(input(f"Board length:\n> "))
                    snakesIn=int(input(f"Number of snakes:\n> "))
                    laddersIn=int(input(f"Number of ladders:\n> "))
                    pawnNumIn=int(input(f"Number of pawns:\n> "))

                    controller(boardLength=lengthIn, snakes=snakesIn, ladders=laddersIn, pawnNum=pawnNumIn)
                    break
                else:
                    print("Incorrect value. Please try again (y/n):")     
    
         # --- Monte Carlo Simulation setup ---
        elif choice == "2":
            print("Monte Carlo Simulation")
            while True:
                default = input("Default settings (y/n):\n> ").capitalize()

                if default == "Y":
                    gamesIn=int(input(f"Number of games:\n> "))

                    controller(gamesNum=gamesIn, verbose=False)
                    break

                elif default == "N":
                    lengthIn=int(input(f"Board length:\n> "))
                    snakesIn=int(input(f"Number of snakes:\n> "))
                    laddersIn=int(input(f"Number of ladders:\n> "))
                    pawnNumIn=int(input(f"Number of pawns:\n> "))
                    gamesIn=int(input(f"Number of games:\n> "))

                    controller(boardLength=lengthIn, snakes=snakesIn, ladders=laddersIn, pawnNum=pawnNumIn, gamesNum=gamesIn, verbose=False)
                    break
                else:
                    print("Incorrect value. Please try again (y/n):")

        elif choice == "3": # Exit
            print("\nThanks for using my program :)")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    menu()
    
