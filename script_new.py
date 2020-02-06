# State Space Search
import copy


# Point class to store coordinates of states
class Point:
    x = -1
    y = -1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y


# File reading
def retrieveData():
    fileobj = open("grid.txt", "r")
    if (fileobj.mode == 'r'):

        # reading rows and cols
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        rows = int(contents[0])
        cols = int(contents[1])

        # initializing array
        maze = [[-1]*cols]*rows

        # reading starting point
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        start_point = Point(int(contents[0]), int(contents[1]))

        # reading ending point
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        goal_point = Point(int(contents[0]), int(contents[1]))

        for i in range(rows):
            contents = fileobj.readline()
            contents = contents.replace("\n", "")
            contents = contents.split(" ")
            maze[i] = [int(i) for i in contents]

        # close file since maze has been initialized now
        fileobj.close()
        return (rows, cols, start_point, goal_point, maze)


# Find path taken to reach goal during BFS
def findPath(maze, path):
    for obj in path:
        maze[obj.x][obj.y] = '*'
    start = path.pop(0)
    maze[start.x][start.y] = 'S'


# Takes a path and computes its cost
def computeCost(path, start_point):

    cost = 0
    init_point = start_point

    for i in range(0, len(path)):
        curr_point = path.pop(0)
        if ((init_point.x - curr_point.x == 0) or (init_point.y - curr_point.y == 0)):
            #up or right
            cost += 2
        else:
            # diagonally up
            cost += 3
        init_point = curr_point

    return cost


def printResults(rows, cols, maze, visitedGoalPoint, cost):
    if (visitedGoalPoint == True):
        maze[goal_point.x][goal_point.y] = 'G'
        for i in range(rows):
            for j in range(cols):
                print(maze[rows-i-1][j], end="     ")
            print('\n')
    else:
        print("Failure! Path not found from start point to goal.")

    print("Total cost = ", cost)


# successor function generation, generates valid points
def successorFunction(rows, cols, element, goal_point, maze, visited):
    vertex = element  # really no need for this lol
    ls = []
    if (vertex.x + 1 < rows and visited[vertex.x + 1][vertex.y] == False and maze[vertex.x+1][vertex.y] == 0):
        # valid
        ls.append(Point(vertex.x + 1, vertex.y))
    if (vertex.y + 1 < cols and visited[vertex.x][vertex.y + 1] == False and maze[vertex.x][vertex.y + 1] == 0):
        # valid
        ls.append(Point(vertex.x, vertex.y + 1))
    if (vertex.x + 1 < rows and vertex.y + 1 < cols and visited[vertex.x + 1][vertex.y + 1] == False and maze[vertex.x + 1][vertex.y + 1] == 0):
        # valid
        ls.append(Point(vertex.x + 1, vertex.y + 1))
    return(ls)


def BFS(rows, cols, start_point, goal_point, maze):

    visited = [[False]*cols for _ in range(rows)]
    queue = []
    path = []
    visited[start_point.x][start_point.y] = True
    goal_found = False

    queue.append([Point(start_point.x, start_point.y)])

    while queue:

        elementary_path = queue.pop(0)
        node = elementary_path[-1]

        if (node == goal_point):
            # goal found
            goal_found = True
            findPath(maze, elementary_path)
            cost = computeCost(elementary_path, start_point)
            printResults(rows, cols, maze, True, cost)
            break

        visited[node.x][node.y] = True

        # generate possible positions
        (valid_moves) = successorFunction(rows, cols, node, goal_point, maze, visited)

        for obj in valid_moves:
            new_path = list(elementary_path)
            new_path.append(obj)
            queue.append(new_path)

    # search ended, goal not found
    if (goal_found == False):
        print("Goal not found!")


# Function to find a path to goal using Depth-First Search
def DFS(rows, cols, start_point, goal_point, maze,depth):
    visited = [[False]*cols for _ in range(rows)]
    cost = 0
    stack = []
    new_path = []
    new_path.append([])
    new_path.append([])
    new_path.append([])
    visited[start_point.x][start_point.y] = True
    goal_found = False

    stack.append([Point(start_point.x, start_point.y)])

    while stack:
        elementary_path = stack.pop(0)
        node = elementary_path[-1]

        if (node == goal_point):
            # goal found
            goal_found = True
            findPath(maze, elementary_path)
            cost = computeCost(elementary_path, start_point)
            printResults(rows, cols, maze, True, cost)
            break

        visited[node.x][node.y] = True

        # generate possible positions
        (valid_moves) = successorFunction(rows, cols, node, goal_point, maze, visited)

        i=0
        for obj in valid_moves:
            new_path[i] = list(elementary_path)
            new_path[i].append(obj)
            i+=1
        length = i
        for x in range(length):
            stack.insert(0,new_path[length-x-1])

    # search ended, goal not found
    if (goal_found == False):
        print("Goal not found!")

#Iterative deepening function, uses DFS with fixed depth
def iterativeDeepening(rows,cols,start_point,goal_point,maze):
    depth = 1
    originalMaze = copy.deepcopy(maze)
    while depth!=20:
        DFS(rows,cols,start_point,goal_point,originalMaze,depth)
        depth+=1

# main program
(rows, cols, start_point, goal_point, maze) = retrieveData()

originalMaze = copy.deepcopy(maze)

input("\nPress Enter to find path using DFS")
DFS(rows,cols,start_point,goal_point,maze,-1)

# input("Press Enter to find path using iterative deepening.")
# (maze,visitedGoalPoint,cost) = iterativeDeepening(rows,cols,start_point,goal_point,originalMaze)

input("\nPress Enter to find path using BFS.")
BFS(rows, cols, start_point, goal_point, originalMaze)
