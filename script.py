#State Space Search


#File reading
fileobj = open("grid.txt", "r")
if (fileobj.mode == 'r'):
    contents = fileobj.read()
    print(contents)
    fileobj.close()