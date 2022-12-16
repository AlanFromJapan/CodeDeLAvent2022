import io
import sys
import re

INPUT_REGEX="Sensor at x=(?P<sx>[^,]+), y=(?P<sy>[^:]+): closest beacon is at x=(?P<bx>[^,]+), y=(?P<by>.+)"

mx = [] 
depth = 0
minX = 100000000
maxX = -100000000
minY = 100000000
maxY = -100000000
#list of segments of the line that we scanned
zaLineScanned=[]
#THE scanned line y coord
L = 10


def showScannedLine ():
    # res = "." * abs(maxX - minX)
    # for seg in zaLineScanned:
    #     if seg[0]-minX >= 0:
    #         res = res[:seg[0]-minX] + ('#' * abs(seg[1] - seg[0])) + res[seg[1]-minX +1:]
    # print (res)
    # counter = sum( [1 if c == "#" else 0 for c in res])
    # print(f"Found { counter } spaces scanned for that line of {len(res)} spots (should be {abs(maxX - minX)} : {minX}~{maxX})")
    
    res = "." * abs(maxX - minX)
    
    for seg in zaLineScanned:
        for x in range(abs(seg[1] - seg[0])):
            p = x + seg[0] - minX
            if p > 0:
                res = res[:p] + '#' + res[p+1:]
    print(res)
    counter = sum( [1 if c == "#" else 0 for c in res])
    print(f"Found { counter } spaces scanned for that line of {len(res)} spots (should be {abs(maxX - minX)} : {minX}~{maxX})")

def overlap(a, b) -> bool:
    return not (a[1] < b[0] or b[1] < a[0])

def union(a,b) :
    if overlap(a,b):
        return [min(a[0], b[0]), max(a[1], b[1])]
    else:
        None

def listUnion(a):
    #https://stackoverflow.com/questions/15273693/union-of-multiple-ranges
    b = []
    for begin,end in sorted(a):
        if b and b[-1][1] >= begin - 1:
            b[-1][1] = max(b[-1][1], end)
        else:
            b.append([begin, end])
    return b

def getCoverage():
    cover = []
    for seg in zaLineScanned:
        if len(cover) == 0:
            cover.append(seg)
        else:
            for i in range(len(cover)):
                c = cover[i]
                if overlap(seg,c):
                    cover[i] = union(seg,c)

    return sum(abs(c[1] -c[0]) for c in cover)



#returns the manhattan distance of 2 points
def getDist(s,b) -> int:
    #thank you https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(s[0] - b[0]) + abs(s[1] - b[1])
    

def show():
    global mx
    for l in mx:
        print("".join(l))

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


sensorNbeacon = []
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

        grp = re.match(INPUT_REGEX, l).groupdict()

        #sensor X, sensorY, beacon X, beacon Y
        sensorNbeacon.append([int(grp["sx"]), int(grp["sy"]), int(grp["bx"]), int(grp["by"])])

        minX = min([minX, int(grp["sx"]), int(grp["bx"])])
        maxX = max([maxX, int(grp["sx"]), int(grp["bx"])])
        minY = min([minY, int(grp["sy"]), int(grp["by"])])
        maxY = max([maxY, int(grp["sy"]), int(grp["by"])])


#print(sensorNbeacon)
print([[minX, maxX], [minY, maxY]])

for snb in sensorNbeacon:
    s = snb[0:2]
    b = snb[2:4]
    d = getDist(s, b)
    #print (f"{s} - {b} : d = {d}")

    #latitude wise, does it crosses the considered line or not?
    if s[1] - d <= L and L <= s[1] + d:
        #in the covered area
        #print(f"  - Overlaps line L {L:,d}") 
        #remove the vertical distance, whatever remains is the horizontal distance
        D = abs(L - s[1]) +1

        #scanned both sides (only X in segment since y is fixed = L)
        segment = [s[0] - D, s[0] + D]
        zaLineScanned.append(segment)

    else:
        #skip this couple sensor/beacon
        pass

print(f"==> {len(zaLineScanned)} Segments scanned of line {L}")
print(zaLineScanned)
showScannedLine()
print(f"Coverage = {sum(abs(c[1] -c[0]) for c in listUnion(zaLineScanned))} vs {getCoverage()}")