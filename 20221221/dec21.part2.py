import io
import sys

filename = "input.txt"
llimit = -1
DBG = False
HUMAN = "humn"

class Node:
    type = "0"
    left = 0
    right = 0
    name = "?"

    def __init__(self, type, name, left, right = 0) -> None:
        self.type = type
        self.left = left
        self.right = right
        self.name = name

    def value(self):
        if self.type == "0":
            #direct
            return int(self.left)
        else:
            if self.type == "+":
                return int(self.left.value()) + int(self.right.value()) 
            elif self.type == "-":
                return int(self.left.value()) - int(self.right.value() )
            elif self.type == "*":
                return int(self.left.value()) * int(self.right.value() )
            elif self.type == "/":
                return int(int(self.left.value()) // int(self.right.value() ))
    
    def __str__(self) -> str:
        return f"[Node n={self.name} t={self.type} l={self.left} r={self.right}]"

    def buildTree(self, dic):
        if self.type == "0":
            return self #done
        
        if isinstance(self.left, str):
            if DBG:
                print(f"Node {self.name} search for left {self.left}")
            self.left = dic[self.left]
            self.left.buildTree(dic)
        
        if isinstance(self.right, str):
            if DBG:
                print(f"Node {self.name} search for right {self.right}")
            self.right = dic[self.right]
            self.right.buildTree(dic)
        
        return self
    
    #returns if searchname is in the subtree of you
    def find(self, searchname)-> bool:
        if self.name == searchname:
            return True
        else:
            if self.type =="0":
                #no kids not me
                return False
            else:
                #reccurse
                return self.left.find(searchname) or self.right.find(searchname)


    #calculate the reverse expected val for Part2
    def targetVal(self, target, otherBranch, onTheLeft, type):
        if type == "+":
            return int(target) - int(otherBranch.value())
        elif type == "-":
            if onTheLeft:
                return int(target) + int(otherBranch.value())
            else:
                return -(int(target) - int(otherBranch.value()))
        elif type == "/":
            if onTheLeft:
                return int(target)  * int(otherBranch.value())
            else:
                return int(otherBranch.value()) // int(target)
        elif type == "*":
            return (int(int(target) // int(otherBranch.value())))        
        
        raise Exception("Shouldn't happen")


    def resolveEquality(self, target):
        global HUMAN
        if self.type == "0":
            #found a wrong leaf, nothing to do
            return
        
        onTheleft = self.left.find(HUMAN)
        humnBranch, otherBranch = (self.left, self.right) if onTheleft else (self.right, self.left)

        if humnBranch.name == HUMAN:
            print(f"FOund it !")
            
            humnBranch.left = self.targetVal(target, otherBranch, onTheleft, self.type)

            print(f">> Value {humnBranch.left:0,d}")
        else:
            humnBranch.resolveEquality(self.targetVal(target, otherBranch, onTheleft, self.type))




#node from job (not int) but with NAMES as L/R
def nodeFromFormula (job, oper):
    formula = job.split(oper)
    node = Node(oper, n, formula[0].strip(), formula[1].strip())
    return node


if len(sys.argv) < 2:
    print("INFO: no filename passed as param, defaulting to 'input.txt'")
else:
    print(f"INFO: 1st param is filename, will process '{sys.argv[1]}'")
    filename = str(sys.argv[1])

if len(sys.argv) >= 3:
    print(f"INFO: 2nd param is limit of lines to process, will process only the first {sys.argv[2]} lines")
    llimit = int(sys.argv[2])



lcount = 0
root = None
nodes = {}
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
        n = l.split(":")[0]
        job = l.split(":")[1].strip()
        node = None
        if "+" in job:
            node = nodeFromFormula(job, "+")
        elif "-" in job:
            node = nodeFromFormula(job, "-")
        elif "*" in job:
            node = nodeFromFormula(job, "*")
        elif "/" in job:
            node = nodeFromFormula(job, "/")
        else:
            #Should be an int
            node = Node("0", n, int(job))
        
        if node == None:
            raise "Shouldn't happen!"
        
        node.name = n
        if node.name == "root":
            root = node

        #store
        nodes[n] = node

#print(root)

print("Building tree")
root = root.buildTree(nodes)
#print(root)

print(f"Root val = {root.value():0,.0f}")
isOnTheLeft = root.left.find(HUMAN)
isOnTheRight = root.right.find(HUMAN)
print(f"{HUMAN} is on the left = {isOnTheLeft} or right = {isOnTheRight}" )

targetVal = 0
targetBranch = None
#target value is on the OTHER side
if isOnTheLeft:
    targetVal = root.right.value()
    targetBranch = root.left
else:
    targetVal = root.left.value()
    targetBranch = root.right
print(f"Need to match value of {targetVal:0,.0f}")

targetBranch.resolveEquality(targetVal)

R = root.right.value()
L = root.left.value()
print(f"After updateing {HUMAN}, then \n  left =  {L:0,d}\n  right = {R:0,d}\n  Diff =  {abs(L) - abs(R):0,d} (l-r)")