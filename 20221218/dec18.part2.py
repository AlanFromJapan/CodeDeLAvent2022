import io
import sys

filename = "input.txt"
llimit = -1
DBG=False

cubes = []
#dict of checked so we don't re-check
checked = {}
bubbles = []

class Kub:
    x=0
    y=0
    z=0
    faces=6
    isAir= False

    def __init__(self, x,y,z, isAir = False) -> None:
        self.x = x
        self.y=y 
        self.z=z
        self.isAir = isAir

    def decFaces(self):
        if self.faces >= 1:
            self.faces = self.faces - 1

    def checkWith(self, k: "Kub"):
        touching = (self.x == k.x and self.y == k.y and abs(self.z - k.z) == 1) or \
            (self.z == k.z and self.y == k.y and abs(self.x - k.x) == 1) or \
            (self.x == k.x and self.z == k.z and abs(self.y - k.y) == 1) 
        
        if touching:
            if DBG:
                print(f"  Touching!")
            #cubes touch so remove 1 face
            self.decFaces()
            k.decFaces()

    def __str__(self) -> str:
        return f"{'AIR' if self.isAir else ''}Kub [{self.x}, {self.y}, {self.z}] ({self.faces} faces)"

    def uid(self)-> str:
        return f"{self.x},{self.y},{self.z}"


#return if k IS an air bubble
def isAirBubble (k: Kub)-> bool:
    global cubes, checked, bubbles
    if k.uid() in checked:
        #leave
        return
    #mark
    checked[k.uid()] = 1

    #air bubble if there's NOT a cube with same uid() AND it has 6 neighbors
    neighbors = 0
    for c in cubes:
        if c.z == k.z and c.x == k.x and c.y == k.y:
            #present in the kubes list
            return False
        if c.z == k.z +1 and c.x == k.x and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z -1 and c.x == k.x and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x +1 and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x -1 and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x and c.y == k.y +1:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x and c.y == k.y-1:
            neighbors = neighbors +1

    #compound bubbles
    for c in bubbles:
        if c.z == k.z +1 and c.x == k.x and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z -1 and c.x == k.x and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x +1 and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x -1 and c.y == k.y:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x and c.y == k.y +1:
            neighbors = neighbors +1
        elif c.z == k.z and c.x == k.x and c.y == k.y-1:
            neighbors = neighbors +1

    if neighbors == 6:
        bubbles.append(k)
    if neighbors > 6:
        raise Exception("WTH more than 6 neighbors??")

    return neighbors == 6



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
        coord = l.split(",")
        k = Kub(int(coord[0]), int(coord[1]), int(coord[2]))
        cubes.append(k)

print(f"Processing list of {len(cubes)} cubes.")
#print([str(c) for c in cubes])
for i in range(len(cubes)):
    ki = cubes[i]
    for j in range(i+1, len(cubes)):
        kj = cubes[j]
        if DBG:
            print(f"Compare {i}:{ki} to {j}:{kj}")
        ki.checkWith(kj)

        if ki.faces == 0:
            #fully covered, no need to check further
            if DBG:
                print(f"  > {i}:{ki} fully covered, skip")
            #break

#print([str(c) for c in cubes])
total = int(sum([int(c.faces) for c in cubes]))
print(f"Total visible {total:0,d} faces over max {6 * len(cubes):0,d} (diff {6 * len(cubes) - total:0,d})")

#part 2 the bubbles
bubblesCount = 0
for c in cubes:
    k = Kub(c.x+1, c.y, c.z)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

    k = Kub(c.x-1, c.y, c.z)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

    k = Kub(c.x, c.y+1, c.z)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

    k = Kub(c.x, c.y-1, c.z)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

    k = Kub(c.x, c.y, c.z+1)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

    k = Kub(c.x, c.y, c.z-1)
    if isAirBubble(k):
        bubblesCount = bubblesCount +1
        print(f"Found bubble {bubblesCount} at {k}")
        continue

print(f"FINISHED: Found total of {bubblesCount} single cube bubblesCount")
print(f"UPDATED Total visible {total - 6 * bubblesCount:0,d} faces over max {6 * len(cubes):0,d} (diff {6 * len(cubes) - (total - 6 * bubblesCount):0,d})")