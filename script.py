#State Space Search

#Point class to store coordinates of states
class Point:
    x = -1
    y = -1
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
#File reading
def retrieveData():
    fileobj = open("grid.txt", "r")
    if (fileobj.mode == 'r'):
        
        #reading rows and cols
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        rows = int(contents[0])
        cols = int(contents[1])

        #initializing array
        maze = [[-1]*cols]*rows

        #reading starting point
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        start_point = Point(int(contents[0]), int(contents[1]))

        #reading ending point
        contents = fileobj.readline()
        contents = contents.replace("\n", "")
        contents = contents.split(" ")
        goal_point = Point(int(contents[0]), int(contents[1])) 
        
        for i in range (rows):
            contents = fileobj.readline()
            contents = contents.replace("\n", "")
            contents = contents.split(" ")
            maze[i] = [int(i) for i in contents]

        #close file since maze has been initialized now   
        fileobj.close()
        return (rows,cols,start_point,goal_point,maze)

#Printing result
def printResults(rows,cols,maze,visitedGoalPoint,cost):
    if (visitedGoalPoint==True):
        maze[goal_point.x][goal_point.y]='G'
        for i in range(rows):
            for j in range(cols):
                print(maze[rows-i-1][j], end = " ")
            print('\n')
    else: print("Failure! Path not found from start point to goal.")
    print("Total cost = ", cost)

#Function to find a path to goal using DFS
def DFS(rows, cols, start_point,goal_point, maze): 
        visited = [[False]*cols for _ in range(rows)]
        cost = 0
        stack = [] 

        vertex = start_point
        stack.append(Point(vertex.x,vertex.y)) 
        visited[(vertex.x)][vertex.y] = True
        maze[(vertex.x)][vertex.y]='S'
  
        while visited[goal_point.x][goal_point.y]!=True: 
            if (vertex.x+1<14 and visited[vertex.x+1][vertex.y]==False and maze[vertex.x+1][vertex.y]==0):
                    stack.append(Point(vertex.x+1,vertex.y)) 
                    vertex.x+=1
                    visited[vertex.x][vertex.y] = True
                    maze[vertex.x][vertex.y]='*'
                    cost+=2
                    costInc = 2
            elif (vertex.y+1<7 and visited[vertex.x][vertex.y+1]==False and maze[vertex.x][vertex.y+1]==0):
                    stack.append(Point(vertex.x,vertex.y+1)) 
                    vertex.y+=1
                    visited[vertex.x][vertex.y] = True
                    maze[vertex.x][vertex.y]='*'
                    cost+=2
                    costInc = 2
            elif (vertex.x+1<14 and vertex.y+1<7 and visited[vertex.x+1][vertex.y+1]==False and maze[vertex.x+1][vertex.y+1]==0):
                    stack.append(Point(vertex.x+1,vertex.y+1)) 
                    vertex.x+=1
                    vertex.y+=1
                    visited[vertex.x][vertex.y] = True
                    maze[vertex.x][vertex.y]='*'
                    cost+=3
                    costInc = 3
            else:
                maze[vertex.x][vertex.y] = 0
                if len(stack) == 0:
                    break
                cost-=costInc
                if (len(stack)!=0):
                    vertex = stack[-1]
                stack = stack[:-1]

        return (maze,visited[goal_point.x][goal_point.y],cost)
        

#main program
(rows,cols,start_point,goal_point,maze) = retrieveData()
(maze,visitedGoalPoint,cost) = DFS(rows,cols,start_point,goal_point,maze)
printResults(rows,cols,maze,visitedGoalPoint,cost)