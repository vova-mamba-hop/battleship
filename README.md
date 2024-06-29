# battleship
TLDR:
My take on the battleship game that in the near and bright future will allow users to swap in their own opponent logic and compare strategies. 

## Foreword

I originally started this project because I thought it would be a neat way of learning and implementing multiarm bandit strategies. Ultimately, I would like to use this project to compare various human based, rule based and machine learning based strategies. I also wanted a more fun way of improving my coding skills that did not involve solving hundreds of leetcode problems. To avoid being immediately discouraged, I did not look at anyone else's battleship code and tried to use as few libraries as I could. AS a result, the code lacks any semblence of elegance and contains an abundance of bugs. With time, I am planning to shift that balance, not sure which way though. 

# Repository Structure

- **src**: contains main script, game functions, and opponent classes (and corresponding functions)
- **parameters**: game parameters such as screen size and various in-game colors and a message file that contains status messages for different stages of the game
- **logs**: at the end of the game you get a log file that will contain ship placements and move history. In the debug mode you get more detailed move by move information with timestamps.

# Installation and Execution

1. Download the repository
2. Make sure that you have pygame package installed. Next update will have a proper requirenment file. 
3. Run python3 main.py in the command line. At first it typically takes a moment to load.
4. Choose an opponent type and whether or not you would like to output a debug log. Debug mode will show you where your opponent places their ships.
5. Enjoy! (try to...)

# Known Issues

- There is still an issue with how computer places ships. Most of the time it is correct, but occassionally it will have one more or one less of a particular ship. Most likely has to do with ships at the boundary.
- Sometimes, there is a delay in recording player's move, which may cause the player to click few time and then computer processes all of those moves all at once.

# Next Update Will:

- have a requirenments file
- detailed instructions for how to add your own opponent

# Afterword

If you get frustrated trying to get it to work, imagine how frustrated I was trying to make it....
