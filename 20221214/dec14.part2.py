import io
import sys

mx = []
depth = 0
maxR = 0
maxL = 1000
sand_start = [500,0]

def show():
    global mx
    for l in mx:
        print("".join(l))

    return

def expand():
    global mx, maxL, maxR
    new = []
    for l in mx:
        new.append(['.'] + l + ['.'])
    
    #add the infinite floor
    new[-1][0] = '#'
    new[-1][-1] = '#'

    maxL = maxL - 1
    maxR = maxR + 1
    mx = new

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


vectors = []
lcount = 0
with io.open(filename, "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if llimit > 0 and lcount > llimit:
        #     break

        #process!
        l = l.strip()

        #edit me v v v v v  
        #print(f"{lcount}: {l}") 
        v = l.split(" -> ")
        for i in range(len(v)-1):
            p1 = [int(v[i].split(",")[0]), int(v[i].split(",")[1])]
            p2 = [int(v[i+1].split(",")[0]), int(v[i+1].split(",")[1])]
            fromto = [p1, p2]
            vectors.append(fromto)

            #max depth
            if p1[1] > depth:
                depth = p1[1]
            if p2[1] > depth:
                depth = p2[1]
            
            if maxL > p1[0]:
                maxL = p1[0]
            if maxL > p2[0]:
                maxL = p2[0]

            if maxR < p1[0]:
                maxR = p1[0]
            if maxR < p2[0]:
                maxR = p2[0]


#print([depth, maxL, maxR])
#init matrix
#depth = +1 for the 0 row with sand source and +2 because part 2
mx = [['.' for _ in range(maxR-maxL+1)] for _ in range(depth +1 +2)]
#######################################################################
# Paint
for v in vectors:
    #draw from P1 (v0)
    if v[0][0] == v[1][0]:
        #horizontal
        dir = -1 if v[1][1] < v[0][1] else 1
        x = v[0][0] - maxL
        y = v[0][1] 
        for i in range(abs(v[0][1] - v[1][1])+1):
            mx[y][x] = "#"
            y = y  + dir

    else:
        #vertical
        dir = -1 if v[1][0] < v[0][0] else 1
        x = v[0][0] - maxL
        y = v[0][1] 
        for i in range(abs(v[0][0] - v[1][0])+1):
            mx[y][x] = "#"
            x = x  + dir

mx[0][500-maxL] = '+'

#add the floor
for i in range(len(mx[0])):
    mx[-1][i] = "#"


count = 0
while True:
    #new grain of sand
    count = count +1
    truex = 500
    y = 0
    #drop
    while True:
        try:
            #TODO CHANGE the logic to a look forward to expan, make sure the x coord is still not impacted, re-loop
            #overflow?
            #recalculated on resize, x is the position in the "window" mx
            x = truex - maxL

            if mx[y +1][x] == '.':
                y = y + 1
            #go left? expand and check at next loop 
            elif x == 0:
                expand()
                continue
            elif mx[y +1][x-1] == '.':
                y = y + 1
                x = x - 1          
                truex = truex -1  
            #go right? expand and check at next loop 
            elif x == len(mx[0])-1:
                expand()
                continue
            elif  mx[y +1][x+1] == '.':
                y = y + 1
                x = x + 1
                truex = truex +1
            else:
                #stuck
                mx[y][x] = 'o'
                if x == 500-maxL and y == 0:
                    show()
                    print(f"Completed at {count}, the answer is {count -1}")
                    exit(0)
                break


        except Exception as ex:
            print(f"x = {x}, y = {y}, count = {count}, depth = {depth}, mxwidth = {len(mx[0])}")
            raise

    #dbg
    if count == llimit:
        show()
        break


