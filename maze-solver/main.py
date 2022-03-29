import argparse

# Initialising global variables
ROWS = 0
COLUMNS = 0
maze = []
sol = []
start = [0,0]
end = [0,0]

# Utility function for validation of coordinates
def isValid(x: int, y: int):
    global ROWS, COLUMNS, maze, sol, end
    if 0 <= x < ROWS and 0 <= y < COLUMNS:
        if maze[x][y].lower() in [' ', 's', 'e']:
            return 1
    return 0

def formatSolution():
    global maze, sol
    for row in range(ROWS):
        for column in range(COLUMNS):
            if sol[row][column] == maze[row][column] and maze[row][column] == ' ':
                sol[row][column] = "X"
            else: sol[row][column] = maze[row][column]
    for row in range(ROWS): sol[row] = "".join(sol[row])

# 
def solveMaze(x: int, y: int):
    global ROWS, COLUMNS, maze, sol, end
    
    # If (x,y) is end return 1
    if x == end[0] and y == end[1] and maze[x][y].lower() == 'e':
        sol[x][y] = ' '
        formatSolution()
        return 1
    
    # Checking if (x,y) is valid for given maze
    if isValid(x, y):
        # Check if current coordinate is already part of solution path
        if sol[x][y] == ' ': return 0

        # Marking (x,y) as a part of solution path
        sol[x][y] = ' '

        # Move down in row
        if solveMaze(x+1, y): return 1

        # If no solution, move right in column
        if solveMaze(x, y+1): return 1

        # If no solution, move up in column
        if solveMaze(x-1, y): return 1

        # If no solution, move left in column
        if solveMaze(x, y-1): return 1

        # If none of above 4 steps work unmark (x,y) as path of solution
        sol[x][y] = '0'
        return 0
    else: return 0
    
# 
ap = argparse.ArgumentParser(description="Maze Solver")
ap.add_argument("-i", "--input", required=True, help="Maze input file")
ap.add_argument("-o", "--output", required=False, default="output.txt", help="Solved Maze output file")

# Builds 'Namespace' object out of the parsed attributes
args = ap.parse_args()

# Opening input file
try:
    with open(args.input, "r") as f:
        maze = f.readlines()
# Handling Error if file not found
except FileNotFoundError:
    print("File doesn\'t exist")
    quit()

# Processing the maze accepted as input argument
maze = list(map(list,maze))
for i in range(len(maze)): 
    if maze[i][-1] == "\n": del maze[i][-1]


# Initialising length counts
ROWS = 0
COLUMNS = 0

# Checking validation
ROWS = len(maze)
rows = set()
for i in range(ROWS): rows.add(len(maze[i]))
if len(rows) != 1:
    print("Invalid Maze: Inconsistent row entries.")
    quit()
else: COLUMNS = list(rows)[0]
S = 0
E = 0
for i in maze:
    for j in i:
        if j.lower() == "s": S+=1
        elif j.lower() == "e": E+=1
error_message = "Invalid Maze: "
if S>1: error_message+="More than one starting point found. "
elif S<1: error_message+="Starting point not found. "
if E>1: error_message+="More than one ending point found. "
elif E<1: error_message+="Ending point not found. "
if S!=1 or E!=1:
    print(error_message)
    quit()

# Initialising maze solution matrix
sol = []
for row in range(ROWS):
    sol.append([])
    for column in range(COLUMNS):
        sol[row].append('0')


# Finding position of start and end
for i in range(ROWS):
    for j in range(COLUMNS):
        if maze[i][j].lower() == "s": start = [i,j]
        elif maze[i][j].lower() == "e": end = [i,j]

# Solving Maze
if solveMaze(start[0], start[1]):
    with open(args.output,"w") as f:
        for row in sol:
            f.write(row+"\n")
    print("Maze Solution:")
    for i in sol: print(i)
else: print("No path found.")