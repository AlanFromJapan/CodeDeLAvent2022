import io
import sys
import re
from graph_tools import Graph

REGEX_PARSE="Valve (?P<valve>[^ ]+) has flow rate=(?P<rate>[^;]+); tunnels? leads? to valves? (?P<leadto>.+)"
MAX_TIME = 30

g = Graph(directed=True)
filename = "input.txt"
llimit = -1
# list of [valve, opened minute, rate]
openedValves = []
currentValve = "AA"
lastAction =""

#take a valve name "AA", "BB" and reutrn a number
def valve2int(valve:str)-> int:
    return ord(valve[0])
def int2valve(i:int)-> str:
    return chr(i) + chr(i)

def totalRelease():
    return sum(x[2] for x in openedValves)

#return next valve, action
def findNextValve(v):
    #TODO logic here :D
    return g.random_vertex(), None


def visit():
    global openedValves, lastAction, currentValve
    for m in range(MAX_TIME):
        print(f"== Minute {m} ==")
        opened = " ".join([x[0] for x in openedValves])
        rel = totalRelease()
        if opened =="":
            print ("No valves are open.")
        else:
            print(f"Valve {opened} are open, releasing {rel} pressure.")
        
        if lastAction =="GO" :
            if not g.get_vertex_attribute(currentValve, "visited") :
                #last step we went to a valve: open it if not 0
                if g.get_vertex_weight(currentValve) > 0:
                    #open
                    openedValves.append([currentValve, m, g.get_vertex_weight(currentValve)])
                    print(f"You open valve {currentValve}")
                #mark as visited
                g.set_vertex_attribute(currentValve, "visited", True)
            else:
                #returning to this point
                print("Just re-passing by.")
            
            lastAction = "OPENED"
        else:
            #GO to another
            next, lastAction = findNextValve(currentValve)
            print(f"You move to valve {next}")
            currentValve = next
            lastAction = "GO"
        

        #next, action = findNextValve(currentValve)

        


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
        try:
            grp = re.match(REGEX_PARSE, l).groupdict()

            #add the vertex. add the weigthed vertices.  The weight is a property of the vertex(node), not the edge
            g.add_vertex(grp["valve"])
            g.set_vertex_weight(grp["valve"], int(grp["rate"]))
            g.set_vertex_attribute(grp["valve"], "visited", False)
            for targetvalve in grp["leadto"].split(","):
                g.add_edge(grp["valve"], targetvalve.strip())
                
        except Exception as ex:
            print("Error parsing:")
            print (ex)
            print(l)

#view graphs at https://graphviz.christine.website/
#print(g)

visit()