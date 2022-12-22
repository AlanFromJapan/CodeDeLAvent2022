import io
import sys
import re


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

# https://pythex.org/
REGEX_DIRECTIONS="([RL]\\d+)"
MX = []
CMD = []
START = []
#possible directrions clockwise from Right
DIRS = [[1,0], [0,1], [-1,0], [0, -1]]
#index of current direction
D = None
#current pos
CUR = []

#get current dir
def currentDir():
    global D, DIRS
    return DIRS[D]

#change current dir
def changeDir(rotation):
    global D, DIRS

    if rotation == "R":
        if D == None:
            D = 0
        else:
            D = (D + 1) % len(DIRS)
    else:
        D = (D - 1) % len(DIRS)

#ok to walk on that cell?
def okCell (c:str)-> bool:
    return c != " " and c != "#"

#move 1 step toward the current direction and return location
def move(start):
    global MX

    target = [start[0] + currentDir()[0], start[1] + currentDir()[1]]
    
    #print(f"  Try to move from {start} -> {target}?")

    ####################################################
    # out of bound -> warp
    #
    if target[1] >= len(MX) or (currentDir()[1] == 1 and MX[target[1]][target[0]] == " "):
        #can wrap vertically bottom to top?
        #top is not a wall so search for first "."
        for y in range(start[1]):
            if MX[y][target[0]] == ".":
                return [target[0], y]
            elif MX[y][target[0]] == "#":
                #stay
                return start
        #if here, no suitable loop so stay
        return start


    if target[1] < 0:
        #can wrap vertically top to bottom?
        for y in range(len(MX) -1, start[1], -1):
            if MX[y][target[0]] == ".":
                return [target[0], y]
            elif MX[y][target[0]] == "#":
                #stay 
                return start
        #if here, no suitable loop so stay
        return start


    if target[0] >= len(MX[target[1]]) or (currentDir()[0] == 1 and MX[target[1]][target[0]] == " "):
        #wrap right to left
        for x in range(len(MX[target[1]])):
            if MX[target[1]][x] == ".":
                return [x, target[1]]
            elif MX[target[1]][x] == "#":
                #stay
                return start
        #if here, no suitable loop so stay
        return start


    if target[0] < 0:
        #wrap left to right
        for x in range(len(MX[target[1]]) -1, start[0], -1):
            if MX[target[1]][x] == ".":
                return [x, target[1]]
            elif MX[target[1]][x] == "#":
                #stay
                return start
        #if here, no suitable loop so stay
        return start 
    
    ####################################################
    # can't move #
    #
    if MX[target[1]][target[0]] == "#":
        #can't move
        return start

    ####################################################
    # can move
    #
    if MX[target[1]][target[0]] == ".":
        return target

    raise Exception("Why are we here?")



#travels for 1 command and returns final location
def travel(start, cmdId):
    global MX, CMD
    
    print(f"Step {cmdId}:")
    curpos = start.copy()

    changeDir(CMD[cmdId][0])

    for s in range (CMD[cmdId][1]):
        newpos = move(curpos)
        print(f"  Moved {currentDir()} from {curpos} -> {newpos}")
        if curpos == newpos:
            #not moved, useless to insist
            break
        curpos = newpos
    
    return curpos
    

def showMX():
    global MX, CUR
    print("+" + "-" * len(MX[0]) + "+")
    for y in range(len(MX)):
        l = MX[y]

        if y == CUR[1]:
            l = l[:CUR[0]] + "@" + l[CUR[0]+1:]
        print(f"|{l}|")
    print("+" + "-" * len(MX[0]) + "+")


lcount = 0
phase = 1
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
        #DO NOT strip the lines by default
        #l = l.strip()

        #edit me v v v v v  
        #print(f"{lcount}: {l}") 
        if phase == 1:
            if l.strip()=="":
                #finished phase 1
                phase = 2
                continue
            MX.append(l[:-1]) #to remove the end of line
        elif phase == 2:
            if l.strip()!="":
                for m in re.findall(REGEX_DIRECTIONS, "R" + l):
                    s = str(m)
                    CMD.append([s[0], int(s[1:])])
                #finished
                break


START = [MX[0].index("."), 0]
CUR = START.copy()

#########################
# Padding of the matrix so that ALL lines have the same length (add spaces on the right). Makes calculation easier
maxlen = -1
for l in MX:
    if len(l) > maxlen:
        maxlen = len(l)

for y in range(len(MX)):
    if len(MX[y]) < maxlen:
        #pad
        MX[y] = MX[y] + " " * (maxlen - len(MX[y]))


showMX()
#let's go, from start, CMD[0]
for step in range(len(CMD)):
    CUR = travel(CUR, step)
showMX()