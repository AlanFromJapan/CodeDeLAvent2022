import io
import sys

snake= [[0, 0], [0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
def head():
    global snake
    return snake[0]
def tail():
    global snake
    return snake[len(snake)-1]

#store positions (x,y) as "x_y", anyway starts at the origin 's'
visitedPositions = ["0_0"]


def show(msg = ""):
    #print(f"{msg}H{head()}-T{tail()}")
    global snake
    res = msg + "H"
    for i in range(len(snake)):
        res = res + "%d:(%d,%d)" % (i, snake[i][0], snake[i][1])
        if not i == len(snake)-1:
            res = res + "="
    print(res)

#record the tail move
def recordTailMove():
    pos = str(tail()[0]) + "_" + str(tail()[1])
    if not pos in visitedPositions:
        visitedPositions.append(pos)

#is snake segment 1 and n+1 within 1 cell distance
#ASSUME: seg is ALWAYS within 0 (head) and len(snake)-2 (the one BEFORE tail)
def within1(seg):
    global snake
    return abs(snake[seg][0] - snake[seg+1][0]) <=1 and abs(snake[seg][1] - snake[seg+1][1]) <=1


#ANYWAY ALWAYS move the HEAD
def moveHead(dir):
    global snake
    if dir == "R":
        #anyway head moves    
        snake[0] = [snake[0][0] +1, snake[0][1]] 

        #propagate reccursively
        moveNextSegment(dir, 0)

    if dir == "U":
        #anyway head moves         
        snake[0] = [snake[0][0], snake[0][1] -1] 

        #propagate reccursively
        moveNextSegment(dir, 0)

    if dir == "L":
        #anyway head moves    
        snake[0] = [snake[0][0] -1, snake[0][1]] 

        #propagate reccursively
        moveNextSegment(dir, 0)

    if dir == "D":
        #anyway head moves         
        snake[0] = [snake[0][0], snake[0][1] +1] 

        #propagate reccursively
        moveNextSegment(dir, 0)


#move the NEXT segment of seg
#ASSUME: seg is ALWAYS within 0 (head) and len(snake)-2 (the one BEFORE tail)
def moveNextSegment(dir, seg):
    global snake
    if dir == "R":
        #still within distance?
        if not within1(seg):
            #must move NEXT SEGMENT: we moved right so NEXT is on the left like that:
            '''
            T..
            T.H
            T..
            '''
            oldPosNextSeg = [snake[seg+1][0], snake[seg+1][1]] #not taking changes with pointers, copy please

            #only possibility for new position is immediately on the left of SEGMENT
            snake[seg+1] = [snake[seg][0] -1, snake[seg][1]]
            
            #if tail moved (we moved seg+1 hence the -2)
            if seg == len(snake) -2:
                recordTailMove()
            else:
                #wait! It's not the end, and we moved one segment, do we need to move NEXT segment?
                # And we need to consider the direction now to trigger the right action for the next segment
                if oldPosNextSeg[1] < snake[seg][1]:
                    #was left and above so moved DOWN
                    moveNextSegment("D", seg+1)
                elif oldPosNextSeg[1] > snake[seg][1]:
                    #was left and below so moved UP
                    moveNextSegment("U", seg+1)
                else:
                    #same level so go right (Same as previous)
                    moveNextSegment(dir, seg+1)


    if dir == "U":
        #still within distance?
        if not within1(seg):
            #must move tail: we moved up so tail is on the bottom like that:
            '''
            .H.
            ...
            TTT
            '''
            oldPosNextSeg = [snake[seg+1][0], snake[seg+1][1]] #not taking changes with pointers, copy please

            #only possibility for new position is immediately on the bottom of head
            snake[seg+1] = [snake[seg][0], snake[seg][1]+1]
            
            #if tail moved (we moved seg+1 hence the -2)
            if seg == len(snake) -2:
                recordTailMove()
            else:
                #wait! It's not the end, and we moved one segment, do we need to move NEXT segment?
                # And we need to consider the direction now to trigger the right action for the next segment
                if oldPosNextSeg[0] < snake[seg][0]:
                    #was left and below so moved RIGHT
                    moveNextSegment("R", seg+1)
                elif oldPosNextSeg[0] > snake[seg][0]:
                    #was right and below so moved LEFT
                    moveNextSegment("L", seg+1)
                else:
                    #same level so go UP (Same as previous)
                    moveNextSegment(dir, seg+1)



    if dir == "L":
        #still within distance?
        if not within1(seg):
            oldPosNextSeg = [snake[seg+1][0], snake[seg+1][1]] #not taking changes with pointers, copy please

            #only possibility for new position is immediately on the left of SEGMENT
            snake[seg+1] = [snake[seg][0] +1, snake[seg][1]]
            
            #if tail moved (we moved seg+1 hence the -2)
            if seg == len(snake) -2:
                recordTailMove()
            else:
                #wait! It's not the end, and we moved one segment, do we need to move NEXT segment?
                # And we need to consider the direction now to trigger the right action for the next segment
                if oldPosNextSeg[1] < snake[seg][1]:
                    #was left and above so moved DOWN
                    moveNextSegment("D", seg+1)
                elif oldPosNextSeg[1] > snake[seg][1]:
                    #was left and below so moved UP
                    moveNextSegment("U", seg+1)
                else:
                    #same level so go right (Same as previous)
                    moveNextSegment(dir, seg+1)


    if dir == "D":
        #still within distance?
        if not within1(seg):
            oldPosNextSeg = [snake[seg+1][0], snake[seg+1][1]] #not taking changes with pointers, copy please

            #only possibility for new position is immediately on the bottom of head
            snake[seg+1] = [snake[seg][0], snake[seg][1]-1]
            
            #if tail moved (we moved seg+1 hence the -2)
            if seg == len(snake) -2:
                recordTailMove()
            else:
                #wait! It's not the end, and we moved one segment, do we need to move NEXT segment?
                # And we need to consider the direction now to trigger the right action for the next segment
                if oldPosNextSeg[0] < snake[seg][0]:
                    #was left and below so moved RIGHT
                    moveNextSegment("R", seg+1)
                elif oldPosNextSeg[0] > snake[seg][0]:
                    #was right and below so moved LEFT
                    moveNextSegment("L", seg+1)
                else:
                    #same level so go UP (Same as previous)
                    moveNextSegment(dir, seg+1)






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
            moveHead(cmd[0])
            show("After : ")
            print("")

            #move(cmd[0])

print (f"Visited {len(visitedPositions)} positions.")