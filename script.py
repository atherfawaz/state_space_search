# State Space Search
import copy
import graphics
from graphics import *


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

# State class that stores a particular state


class State:
    elementary_path = []
    node = Point(-1, -1)
    currDepth = -1

    def __init__(self, path, depth, node):
        self.currDepth = depth
        self.elementary_path = path
        self.node = node

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


# Find path taken to reach goal during searching algorithms
def plotPath(maze, path):
    for obj in path:
        maze[obj[0].x][obj[0].y] = '*'
    start = path.pop(0)
    maze[start[0].x][start[0].y] = 'S'
    maze[goal_point.x][goal_point.y] = 'G'


# Takes a path and computes its cost
def computeCost(path, start_point):

    cost = 0
    init_point = start_point

    for i in range(0, len(path)):
        curr_point = path.pop(0)
        if ((init_point.x - curr_point[0].x == 0) or (init_point.y - curr_point[0].y == 0)):
            #up or right
            cost += 2
        else:
            # diagonally up
            cost += 3
        init_point = curr_point[0]

    return cost


def printResults(rows, cols, maze, cost, visitedGoalPoint, graphTitle):
    win = GraphWin(graphTitle, 700, 700)
    block_size = 35
    start_x = 200
    start_y = 100
    starting_x = 600
    starting_y = 210
    startPointMessage = Text(graphics.Point(
        575, 125), "Start index is [{}, {}]".format(start_point.x, start_point.y))
    goalPointMessage = Text(graphics.Point(
        575, 150), "Goal index is [{}, {}]".format(goal_point.x, goal_point.y))
    completionMessage = Text(graphics.Point(575, 175), "Path exists!")
    errorMessage = Text(graphics.Point(575, 175), "No path exists!")
    costMessage = Text(graphics.Point(575, 200),
                       "The cost for this path is {}".format(cost))
    noteMessage = Text(graphics.Point(
        575, 500), "Note: If goal and obstacle\n are overlapping, goal won't\n be visible.")

    legendWord = Text(graphics.Point(575, 250), "Legend:")
    legendWords = Text(graphics.Point(575, 350),
                       "Start Point\n\nEnd Point\n\nPath\n\nObstacle")
    blocky = Rectangle(graphics.Point(starting_x+(1*block_size), starting_y+(2*block_size)),
                       graphics.Point(starting_x+(1*block_size)+block_size, starting_y+(2*block_size)+block_size))
    blocky.setFill("yellow")
    blocky2 = Rectangle(graphics.Point(starting_x+(1*block_size), starting_y+(3*block_size)),
                        graphics.Point(starting_x+(1*block_size)+block_size, starting_y+(3*block_size)+block_size))
    blocky2.setFill("green")
    blocky3 = Rectangle(graphics.Point(starting_x+(1*block_size), starting_y+(4*block_size)),
                        graphics.Point(starting_x+(1*block_size)+block_size, starting_y+(4*block_size)+block_size))
    blocky3.setFill("blue")
    blocky4 = Rectangle(graphics.Point(starting_x+(1*block_size), starting_y+(5*block_size)),
                        graphics.Point(starting_x+(1*block_size)+block_size, starting_y+(5*block_size)+block_size))
    blocky4.setFill("red")

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            block = Rectangle(graphics.Point(start_x + (j * block_size), start_y + (i * block_size)),
                              graphics.Point(start_x + (j * block_size) + block_size, start_y + (i * block_size) + block_size))
            if maze[rows-i-1][j] == 1:
                block.setFill("red")
            elif rows-i-1 == start_point.x and j == start_point.y:
                block.setFill("yellow")
            elif maze[rows-i-1][j] == '*':
                block.setFill("blue")
            elif rows-i-1 == goal_point.x and j == goal_point.y:
                block.setFill("green")
            block.draw(win)

    blocky.draw(win)
    blocky2.draw(win)
    blocky3.draw(win)
    blocky4.draw(win)
    startPointMessage.draw(win)
    goalPointMessage.draw(win)
    noteMessage.draw(win)
    legendWord.setStyle("bold")
    legendWord.setTextColor("purple")
    legendWord.draw(win)
    legendWords.draw(win)
    if (visitedGoalPoint):
        completionMessage.setStyle("bold")
        completionMessage.draw(win)
        costMessage.draw(win)
    else:
        errorMessage.setStyle("bold")
        errorMessage.draw(win)


# successor function generation, generates valid points
def successorFunction(rows, cols, element, goal_point, maze, visited):

    vertex = element  # really no need for this lol
    ls = []
    # our personal priority, down, right, diagonal (right,down)
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
    visited[start_point.x][start_point.y] = True
    goal_found = False

    # dummy state
    state = State([], -1, Point(-1, -1))

    x = []
    x.append([Point(start_point.x, start_point.y), -1])
    queue.append(x)

    while queue:

        # state variables
        state.currDepth = -1
        state.elementary_path = queue.pop(0)
        state.node = state.elementary_path[-1][0]
        # state variables

        if (state.node == goal_point):
            # goal found
            goal_found = True
            plotPath(maze, state.elementary_path)
            cost = computeCost(state.elementary_path, start_point)
            printResults(rows, cols, maze, cost, True, "BFS")
            break

        visited[state.node.x][state.node.y] = True

        # generate possible positions
        (valid_moves) = successorFunction(
            rows, cols, state.node, goal_point, maze, visited)

        for obj in valid_moves:
            new_path = list(state.elementary_path)
            new_path.append([obj, -1])
            queue.append(new_path)

    # search ended, goal not found
    if (goal_found == False):
        printResults(rows, cols, maze, 0, False, "BFS")


# Function to find a path to goal using Depth-First Search
def DFS(rows, cols, start_point, goal_point, maze, depth):
    visited = [[False]*cols for _ in range(rows)]
    cost = 0
    currDepth = 0
    stack = []
    new_path = []
    new_path.append([])
    new_path.append([])
    new_path.append([])
    visited[start_point.x][start_point.y] = True
    goal_found = False

    # dummy state
    state = State([], -1, Point(-1, -1))

    x = []
    x.append([Point(start_point.x, start_point.y), currDepth])
    stack.append(x)

    #stack.append([Point(start_point.x, start_point.y)],currDepth)

    while stack:

        # state variables
        state.elementary_path = stack.pop(0)
        state.node = state.elementary_path[-1][0]
        state.currDepth = state.elementary_path[-1][-1]
        # state variables

        if (state.node == goal_point):
            # goal found
            goal_found = True
            plotPath(maze, state.elementary_path)
            cost = computeCost(state.elementary_path, start_point)
            if depth == -1:
                printResults(rows, cols, maze, cost, True, "DFS")
            else:
                printResults(rows, cols, maze, cost,
                             True, "IterativeDeepening")
            break

        visited[state.node.x][state.node.y] = True

        # generate possible positions
        (valid_moves) = successorFunction(
            rows, cols, state.node, goal_point, maze, visited)
        if (state.currDepth < depth or depth == -1):
            i = 0
            for obj in valid_moves:
                new_path[i] = list(state.elementary_path)
                new_path[i].append([obj, state.currDepth + 1])
                i += 1
            length = i
            for x in range(length):
                stack.insert(0, new_path[length-x-1])

    # search ended, goal not found
    if (goal_found == False and depth == -1):
        printResults(rows, cols, maze, 0, False, "DFS")
    elif (goal_found):
        return True
    else:
        return False


# Iterative deepening function, uses DFS with fixed depth
def iterativeDeepening(rows, cols, start_point, goal_point, maze):
    depth = 1
    goal_found = False
    originalMaze = copy.deepcopy(maze)
    while depth != 15 and goal_found == False:
        goal_found = DFS(rows, cols, start_point,
                         goal_point, originalMaze, depth)
        depth += 1
    if not goal_found:
        printResults(rows, cols, maze, 0, False, "Iterative Deepening")


# main program
(rows, cols, start_point, goal_point, maze) = retrieveData()

originalMaze = copy.deepcopy(maze)

input("\nPress Enter to find path using Depth-First Search.")
DFS(rows, cols, start_point, goal_point, maze, -1)

input("\nPress Enter to find path using Iterative Deepening.")
iterativeDeepening(rows, cols, start_point, goal_point, originalMaze)

input("\nPress Enter to find path using Breadth-First Search.")
BFS(rows, cols, start_point, goal_point, originalMaze)

input("\nPress Enter to exit")
