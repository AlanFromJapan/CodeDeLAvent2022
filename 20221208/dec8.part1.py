import io
import sys


def isVisible(mx, x, y):
    #1: borders?
    if x == 0 or y == 0 or x == len(mx[0])-1 or y == len(mx) -1:
        return True

    #2: top?
    safe = False
    for r in range(y):
        if mx[r][x] >= mx[y][x]:
            safe = True
    if not safe:
        print (f"({x}, {y}) visible from TOP")
        return True 

    #3: bottom?
    safe = False
    for r in range(len(mx)-1, y, -1):
        if mx[r][x] >= mx[y][x]:
            safe = True
    if not safe:
        print (f"({x}, {y}) visible from BOTTOM")
        return True 

    #4: left?
    safe = False
    for c in range(x):
        if mx[y][c] >= mx[y][x]:
            safe = True
    if not safe:
        print (f"({x}, {y}) visible from LEFT")
        return True 

    #5: right?
    safe = False
    for c in range(len(mx[0])-1, x, -1):
        if mx[y][c] >= mx[y][x]:
            safe = True
    if not safe:
        print (f"({x}, {y}) visible from RIGHT")
        return True 

    #you're well hidden
    return False



##############################################################################################################
filename = "input.txt"
llimit = -1
if len(sys.argv) < 2:
    print("INFO: no filename passed as param, defaulting to 'input.txt'")
else:
    print(f"INFO: 1st param is filename, will process '{sys.argv[1]}'")
    filename = str(sys.argv[1])

if len(sys.argv) >= 3:
    print(f"INFO: 2nd param is limit of lines to process, will process only the first {sys.argv[2]} lines")
    llimit = int(sys.argv[2])

mx = []
lcount = 0
with io.open(filename, "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        if llimit > 0 and lcount > llimit:
            break

        #process!
        l = l.strip()

        #add the line as a list of char (not string) with the [*_string_] syntax
        mx.append([*l])

print (mx)

totalVisible = 0
for x in range(len(mx[0])):
    for y in range(len(mx)):
        visible = isVisible(mx,x,y)
        #print (f"({x}, {y}) visible")
        totalVisible = totalVisible + (1 if visible else 0)

print (f"Total visible is {totalVisible}.")
