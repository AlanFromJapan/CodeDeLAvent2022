import io
import sys

#default is 1000
sys.setrecursionlimit(10000)

MAX_POINTBREAK = 10000
pointBreak = 0
debug = False

class Nod():
    X = 0
    Y = 0
    children = []
    isTheEnd = False

    def __init__(self, x, y, isTheEnd = False) -> None:
        self.X = x
        self.Y = y
        self.children = []
        self.isTheEnd = isTheEnd
    
    #WTH python I must put a string when typing params of the same class?!
    def addChild(self, n:"Nod"):
        self.children.append(n)
    
    def mapVal(x:int, y:int) ->str:
        global zaMapShadow
        return zaMapShadow[y][x] if y >= 0 and y < len(zaMapShadow) and x >= 0 and x < len(zaMapShadow[0]) else "."

    def canGo(_from:str, _to:str):
        #return _to != "." and ((_from == "S" and _to =="a")  or abs(ord(_from) - ord(_to)) <= 1)
        return _to != "." and ((_from == "S" and _to =="a")  or ord(_to) - ord(_from) <= 1)

    def maxTreeDepth(self):
        maxChild = 0
        for c in self.children:
            d = c.maxTreeDepth()
            if d > maxChild:
                maxChild = d

        return 1 + maxChild
        
    def pathToGoal(self)-> int:
        global zaMap
        if self.isTheEnd:
            print("E !")
            return 1
        else:
            minChild = 999999999999999
            for c in self.children:
                d = c.pathToGoal()
                if d < minChild:
                    minChild = d
            if not minChild == 999999999999999:
                print(f"{zaMap[self.Y][self.X]} ({self.Y},{self.X})")
                zaMapShadow[self.Y][self.X] = "*"
                return 1 + minChild
            else:
                return 999999999999999

    #THE recursion
    def searchPath(self) -> bool:
        global zaMapShadow
        global pointBreak, MAX_POINTBREAK
        global debug

        myVal = Nod.mapVal(self.X, self.Y)

        #debug
        if pointBreak >= MAX_POINTBREAK:
            #print the shadow and exit
            for l in zaMapShadow:
                print("".join(l))
            
            print(f"Tree depth max is {root.maxTreeDepth()}")
            root.pathToGoal()
            exit()
        pointBreak = pointBreak + 1
        
        if debug:
            print(f"Nod ({self.X}, {self.Y}):")

        #Am I the end?
        if myVal == "z":
            self.isTheEnd = True

            if debug:
                print(f"  the End!")
            return True
        
        #can I go anywhere?
        if not Nod.canGo(myVal, Nod.mapVal(self.X +1, self.Y)) \
            and not Nod.canGo(myVal, Nod.mapVal(self.X, self.Y +1)) \
            and not Nod.canGo(myVal, Nod.mapVal(self.X -1, self.Y)) \
            and not Nod.canGo(myVal, Nod.mapVal(self.X , self.Y -1)) :
            #dead end...
            if debug:
                print(f"  Dead end :(")
            return False
        
        #ok so not the end and I can go somewhere so go!
        #mark my place
        zaMapShadow[self.Y][self.X] = "."

        if Nod.canGo(myVal, Nod.mapVal(self.X +1, self.Y)):
            n = Nod(self.X +1, self.Y)
            if n.searchPath():
                self.addChild(n)
                return True
        if Nod.canGo(myVal, Nod.mapVal(self.X , self.Y+1)):
            n = Nod(self.X, self.Y+1)
            if n.searchPath():
                self.addChild(n)
                return True
        if Nod.canGo(myVal, Nod.mapVal(self.X -1, self.Y)):
            n = Nod(self.X -1, self.Y)
            if n.searchPath():
                self.addChild(n)
                return True
        if Nod.canGo(myVal, Nod.mapVal(self.X , self.Y-1)):
            n = Nod(self.X, self.Y-1)
            if n.searchPath():
                self.addChild(n)
                return True

        #unmark? No, don't search ALL path, one is enough
        #zaMapShadow[self.Y][self.X] = myVal

        #well it didn't work
        return False


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
print(f"Tree depth max is {root.maxTreeDepth()}")
root.pathToGoal()

for l in zaMapShadow:
    print("".join(l))
