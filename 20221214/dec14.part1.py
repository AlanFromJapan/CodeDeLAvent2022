import io
import sys

mx = [] #[['.'] *mx_cols ] *mx_rows
depth = 0
maxR = 0
maxL = 1000
sand_start = [500,0]

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
mx = [['.' for _ in range(maxR-maxL+1)] for _ in range(depth +1)]
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

count = 0
while True:
    #new grain of sand
    count = count +1
    x = 500 - maxL
    y = 1
    #drop
    while True:
        try:
            #overflow?
            ovf = False
            if y == depth:
                ovf = True
            #can move?
            elif mx[y +1][x] == '.':
                y = y + 1
            elif x == 0:
                ovf = True
            elif x > 0 and mx[y +1][x-1] == '.':
                y = y + 1
                x = x - 1
            elif x < len(mx[0]) -1 and mx[y +1][x+1] == '.':
                y = y + 1
                x = x + 1
            else:
                #stuck
                mx[y][x] = 'o'
                break

            if ovf:
                show()
                print(f"Overflow at {count}, the answer is {count -1}")
                exit(0)
        except Exception as ex:
            print(f"x = {x}, y = {y}, count = {count}, depth = {depth}, mxwidth = {len(mx[0])}")
            raise

    #dbg
    if count == llimit:
        show()
        break


