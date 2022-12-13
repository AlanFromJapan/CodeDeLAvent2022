import io
import sys

#return if in right order
def compare(left, right) -> bool:
    print (f"- Compare {left} vs {right}")
    if len(left) == 0:
        return True
    if len(right) == 0:
        #here len(left) is not 0 so there's items on the left so rule says if you went here it was ok so all is ok
        return True
    
    g = left[0]
    d = right[0]

    if type(g) == type(d) and type(g) == int:
        #int to int
        if g > d:
            #bad
            return False
        #ok so continue
        return compare(left[1:], right[1:])

    if type(g) == type(d) and type(g) == list:
        #list to list
        return compare(g, d) and compare(left[1:], right[1:])
    
    #assume list to int
    if type(g) == int:
        g = [g]
    if type(d) == int:
        d = [d]
    return compare(g, d) and compare(left[1:], right[1:])


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


L = []
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
        if l != "":
            L.append(eval(l))

# print("data:")
# for l in L:
#     print(l)

for i in range(len(L)//2):
    print(f"========== Pair {i+1} ===========")
    result = compare(L[i*2], L[i*2+1])
    print(f"Sorted ok = {result}")