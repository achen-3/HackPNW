# Micah Lam
# Nim Game 
# Vs Code

import random, os; from colorama import Fore, Style #with os imported on mac, I used 'cls' instead of cls for windows
os.system('cls')
print("Welcome to Nim!")
stones = random.choice([i for i in range(22, 32) if i % 4 != 0])

print("There are " + str(stones) + " stones on the board.\n")
#Functions
def ComputerTurn():
	# Pre: stones has to be global to continue updating
	# Post: Gives the computer output into the game
	global stones
	print("Computer's turn.")
	if stones == 1:
		stonestaken = 1
	elif stones <= 4:
		stonestaken = stones - 1
	else:
		stonestaken = (stones - 1) % 4 if (stones - 1) % 4 != 0 else 3
	print("Computer takes " + Fore.RED + str(stonestaken) + Style.RESET_ALL + " stone(s).")
	stones -=stonestaken
	print("There are " + Fore.GREEN + str(stones) + Style.RESET_ALL + " stones on the board.")
	return stones <= 0

def PlayerTurn():
	# Pre: stones has to be global to continue updating
	# Post: Gives the player output into the game
	global stones
	print("Your turn.")
	stonestaken = int(input("Take 1, 2, or 3 stones: "))
	while stonestaken < 1 or stonestaken > 3 or stonestaken > stones:
		print("Invalid number of stones. Try again.")
		stonestaken = int(input("Take 1, 2, or 3 stones: "))
	stones -= stonestaken
	print("There are " + Fore.GREEN + str(stones) + Style.RESET_ALL + " stones on the board.")
	os.system('cls')
	print("Game of Nim")
	return stones <= 0 

	


def NimGame(stones):
	# Pre: stones has to be global to continue updating
	# Post: Starts and ends the game/ main game loop
	ilovetogamble = random.randint(0, 1)
	while stones > 0:
		if ilovetogamble == 0:
			if ComputerTurn():
				print("You took the last stone. You lose!")
				break
			if PlayerTurn():
				print("Computer Wins")
				break
		else:
			if PlayerTurn():
				print("Computer Wins")
				break
			if ComputerTurn():
				print("You Win!")
				break
NimGame(stones)