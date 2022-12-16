import io
import sys

Debug = True
def debug(s):
    if Debug:
        print("DBG: " + str(s))


#return if in right order
def compare(left, right, lastWasEqual = False) -> bool:
    print (f"- Compare {left} vs {right}")
    if len(left) == 0:
        debug("Stop: left is empty - Ok")
        return True
    if len(right) == 0:
        debug(f"Stop: Right is empty - {not lastWasEqual}")
        #here len(left) is not 0 so there's items on the left so rule says if you went here it was ok so all is ok
        return not lastWasEqual
    
    g = left[0]
    d = right[0]
    debug(f"g ({g}) > d ({d})")

    if type(g) == type(d) and type(g) == int:
        debug("int 2 int")
        #int to int
        if g > d:
            #bad
            print("g>d")
            return False
        #ok so continue
        
        print("g<=d : rec")
        return compare(left[1:], right[1:], g == d)

    if type(g) == type(d) and type(g) == list:
        print("list 2 list : rec")
        #list to list
        return compare(g, d) and len(right) > 0 and compare(left[1:], right[1:])
    
    #assume list to int
    if type(g) == int:
        g = [g]
    if type(d) == int:
        d = [d] 
    print("list 2 int : rec")
    return compare(g, d) and len(right) > 0 and compare(left[1:], right[1:], g[0] == d[0])


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

summary = []
expects = [[1, True], [2, True], [3, False], [4, True], [5, False], [6, True], [7, False], [8, False]]
for i in range(len(L)//2):
    print(f"========== Pair {i+1} ===========")
    result = compare(L[i*2], L[i*2+1])
    print(f"Sorted ok = {result}")

    summary.append([i+1, result])

print(f"Summary: {summary}")
print(f"Expects: {expects}")
