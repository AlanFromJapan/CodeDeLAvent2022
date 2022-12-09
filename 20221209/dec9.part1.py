import io
import sys

head = [0, 0]
tail = [0, 1]
#store positions (x,y) as "x_y", anyway starts at the origin 's'
visitedPositions = ["0_0"]


def show(msg = ""):
    global head
    global tail
    print(f"{msg}H{head}-T{tail}")

#record the tail move
def recordTailMove():
    global tail
    pos = str(tail[0]) + "_" + str(tail[1])
    if not pos in visitedPositions:
        visitedPositions.append(pos)

def tailWithin1():
    global head
    global tail
    return abs(head[0] - tail[0]) <=1 and abs(head[1] - tail[1]) <=1

#move ONCE in that direction
def move(dir):
    global head
    global tail
    if dir == "R":
        #anyway head moves         
        head = [head[0] + 1, head[1]]

        #still within distance?
        if not tailWithin1():
            #must move tail: we moved right so tail is on the left like that:
            '''
            T..
            T.H
            T..
            '''
            #only possibility for new position is immediately on the left of head
            tail = [head[0] -1, head[1]]
            recordTailMove()
        #done
        return

    if dir == "U":
        #anyway head moves         
        head = [head[0], head[1]-1]

        #still within distance?
        if not tailWithin1():
            #must move tail: we moved up so tail is on the bottom like that:
            '''
            .H.
            ...
            TTT
            '''
            #only possibility for new position is immediately on the bottom of head
            tail = [head[0], head[1]+1]
            recordTailMove()
        #done
        return

    if dir == "L":
        #anyway head moves         
        head = [head[0] - 1, head[1]]

        #still within distance?
        if not tailWithin1():
            tail = [head[0] +1, head[1]]
            recordTailMove()
        #done
        return
            

    if dir == "D":
        #anyway head moves         
        head = [head[0], head[1]+1]

        #still within distance?
        if not tailWithin1():
            tail = [head[0], head[1]-1]
            recordTailMove()
        #done
        return




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

        #edit me v v v v v  
        #print(f"{lcount}: {l}") 
        cmd = l.split (" ")
        
        for step in range(int(cmd[1])):
            print(f"Move to {cmd[0]}!")
            show("Before : ")
            move(cmd[0])
            show("After : ")
            print("")

            #move(cmd[0])

print (f"Visited {len(visitedPositions)} positions.")