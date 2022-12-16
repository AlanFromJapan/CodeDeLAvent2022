import io
import sys

#default is 1000
#sys.setrecursionlimit(10000)

debug = False
zaMap = []
zaMapCount = []
start = []
goal = []

def showMap(m):
    for l in m:
        print("".join([" " + str(x) for x in l]))

def showMapCount():
    global zaMapCount
    for l in zaMapCount:
        print(" ".join([" . " if x == -1 else f"{x: 3d}" for x in l]))

def canGo(_from:str, _to:str) -> bool:
    res = _to != "." and ((_from == "S" and _to =="a") or (_from == "z" and _to =="E")  or (_to != "E" and (ord(_to) - ord(_from)) <= 1))
    return res

#start from goal, mark as 0, then walk back each round and add +1 until found start
def breadthFirst(rount=0):
    global zaMapCount, zaMap, start, goal

    # if(rount == 20):
    #     print("DBG: BREAK RECURSION!")
    #     return

    for y in range(len(zaMapCount)):
        for x in range(len(zaMapCount[0])):
            if zaMapCount[y][x] != -1:
                #already done, move next
                continue
            if      (x == len(zaMapCount[0])-1 or zaMapCount[y][x+1] == -1) \
                and (x == 0 or zaMapCount[y][x-1] == -1) \
                and (y == len(zaMapCount)-1 or zaMapCount[y+1][x] == -1) \
                and (y == 0 or zaMapCount[y-1][x] == -1) :
                #surrounded by borded OR unprocessed: skip
                continue
        
            #so here we aren't in a special case and a neighbor is not null
            minNeighbor = 100000000000000000000000
            neighbors = []
            if x < len(zaMapCount[0])-1 and zaMapCount[y][x+1] != -1 and canGo(zaMap[y][x], zaMap[y][x+1]):
                neighbors.append(zaMapCount[y][x+1])
            if x > 0 and zaMapCount[y][x-1] != -1 and canGo(zaMap[y][x], zaMap[y][x-1]):
                neighbors.append(zaMapCount[y][x-1])
            if y < len(zaMapCount)-1 and zaMapCount[y+1][x] != -1  and canGo(zaMap[y][x], zaMap[y+1][x]):
                neighbors.append(zaMapCount[y+1][x])
            if y > 0 and zaMapCount[y-1][x] != -1 and canGo(zaMap[y][x], zaMap[y-1][x]):
                neighbors.append(zaMapCount[y-1][x])
            
            if len(neighbors) > 0:
                #there is a possible move
                minNeighbor = min(neighbors)
                zaMapCount[y][x] = minNeighbor + 1
                    

    if zaMapCount[start[1]][start[0]] != -1:
        #processed goal, we're done
        print (f"Found a result in {rount} rounds.")
        return zaMapCount[start[1]][start[0]]
    else:
        #and again until meet the start
        return breadthFirst(rount +1)

        


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
        zaMap.append([* l])
        zaMapCount.append([-1 for _ in range(len(l))])


row = 0
for l in zaMap:
    #print(l)
    if "S" in l:
        start = [l.index("S") ,  row]
    if "E" in l:
        goal = [l.index("E") ,  row]
    row = row + 1

print(f"Start at {start}, go to {goal}")

#showMap(zaMap)

#goal is zero
zaMapCount[goal[1]][goal[0]] = 0
breadthFirst()

#showMap(zaMapCount)
showMapCount()

print(f"DONE! The path is {zaMapCount[start[1]][start[0]]} steps long")

