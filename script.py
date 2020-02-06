#State Space Search
class Point:
    x = -1
    y = -1
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
#File reading
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