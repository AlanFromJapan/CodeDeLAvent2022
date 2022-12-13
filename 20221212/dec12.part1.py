import io
import sys

#default is 1000
sys.setrecursionlimit(10000)

MAX_POINTBREAK = 2000000
pointBreak = 0
debug = False

class Nod():
    X = 0
    Y = 0
    children = []
    isTheEnd = False
    depth = -1

    def __init__(self, x, y, isTheEnd = False) -> None:
        self.X = x
        self.Y = y
        self.children = []
        self.isTheEnd = isTheEnd
        self.depth = -1

    
    #WTH python I must put a string when typing params of the same class?!
    def addChild(self, n:"Nod"):
        self.children.append(n)
    
    def mapVal(x:int, y:int) ->str:
        global zaMapShadow
        return zaMapShadow[y][x] if y >= 0 and y < len(zaMapShadow) and x >= 0 and x < len(zaMapShadow[0]) else "."

    def canGo(_from:str, _to:str) -> bool:
        res = _to != "." and ((_from == "S" and _to =="a") or (_from == "z" and _to =="E")  or (_to != "E" and (ord(_to) - ord(_from)) <= 1))
        return res

    def canGoXY (_from:str, x:int, y:int) -> bool:
        return Nod.canGo(_from, Nod.mapVal(x, y))

    # def maxTreeDepth(self):
    #     maxChild = 0
    #     for c in self.children:
    #         d = c.maxTreeDepth()
    #         if d > maxChild:
    #             maxChild = d

    #     return 1 + maxChild
        
    # def pathToGoal(self)-> int:
    #     global zaMap
    #     if self.isTheEnd:
    #         print("E !")
    #         return 1
    #     else:
    #         minChild = 999999999999999
    #         for c in self.children:
    #             d = c.pathToGoal()
    #             if d < minChild:
    #                 minChild = d
    #         if not minChild == 999999999999999:
    #             print(f"{zaMap[self.Y][self.X]} ({self.X},{self.Y})")
    #             zaMapShadow[self.Y][self.X] = "*"
    #             return 1 + minChild
    #         else:
    #             return 999999999999999


    #THE recursion, returns bool if path or not, and  depth to Goal or -1 if deadend
    def searchPath(self):
        global zaMapShadow
        global pointBreak, MAX_POINTBREAK
        global debug

        myVal = Nod.mapVal(self.X, self.Y)

        #debug to process bit by bit 
        if pointBreak >= MAX_POINTBREAK:
            #print the shadow and exit
            for l in zaMapShadow:
                print("".join(l))
            
            print(f"Tree depth max is {root.depth}")
            #root.pathToGoal()
            print (":( Pointbreak :(")
            exit()
        pointBreak = pointBreak + 1


        #finished?
        if myVal == "E":
            if debug:
                print("Goal!")
            #finished
            self.depth = 0
            self.isTheEnd = True
            return True, 0, self
        
        if myVal == ".":
            #nope
            self.depth = -1
            return False, -1, None

        #let reccurse
        #mark
        zaMapShadow[self.Y][self.X] = "."

        ok = False
        dmin = 999999999999999999
        nmin = None
        if Nod.canGoXY(myVal, self.X +1, self.Y):
            ok, d, n = Nod(self.X +1, self.Y).searchPath() 
            if ok and dmin > d and n != None:
                dmin = d
                nmin = n
        if Nod.canGoXY(myVal, self.X , self.Y+1):
            ok, d, n = Nod(self.X, self.Y+1).searchPath() 
            if ok and dmin > d and n != None:
                dmin = d
                nmin = n
        if Nod.canGoXY(myVal, self.X -1, self.Y):
            ok, d, n = Nod(self.X -1, self.Y).searchPath() 
            if ok and dmin > d and n != None:
                dmin = d
                nmin = n
        if Nod.canGoXY(myVal, self.X , self.Y-1) :
            ok, d, n = Nod(self.X , self.Y-1).searchPath()
            if ok and dmin > d and n != None:
                dmin = d
                nmin = n

        #unmark
        zaMapShadow[self.Y][self.X] = myVal

        #found a path?
        if nmin != None:
            self.addChild(nmin)
            self.depth = dmin +1
            return True, self.depth, self
        else:
            #no path
            return False, -1, None



        


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


zaMap = []
zaMapShadow = []
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
        zaMapShadow.append([* l])

start = []
goal = []
row = 0
for l in zaMap:
    #print(l)
    if "S" in l:
        start = [l.index("S") ,  row]
    if "E" in l:
        goal = [l.index("E") ,  row]
    row = row + 1

print(f"Start at {start}, go to {goal}")

root = Nod(start[0], start[1])

root.searchPath()


print("Finished!")
#root.pathToGoal()

# for l in zaMapShadow:
#     print("".join(l))

print(f"Tree depth max is {root.depth}")