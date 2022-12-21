import io
import sys

filename = "input.txt"
llimit = -1
DBG = False

#the current list of numbers 
L = []
#by index where they were in the ORIGINAL data
I = []

#Rotate both the values L and index I according the I[ipos]
def rotate(ipos):
    global L, I
    lpos = ipos
    val = L[lpos]
    newpos = lpos

    newpos = lpos+ val

    if newpos > len(L):
        if DBG:
            print(f"overflow: newpos {newpos} > len {len(L)}")
        newpos = newpos % len(L) +1
        
        if DBG:
            print(f"  > off {newpos} ")

    if DBG:
        print(f">> ipos={ipos}, lpos={lpos}, val={val}, newpos={newpos}")

    #remove value
    L = L[:lpos] + L[lpos+1:]
    I = I[:ipos] + I[ipos+1:]

    #insert value (don't care of original pos anymore hence -1)
    L= L[:newpos] + [val] + L[newpos:]
    I= I[:newpos] + [-1] + I[newpos:]


def calcResult():
    global L
    zero = L.index(0)
    print(f"1000th = {L[(zero + 1000)% len(L)]}")
    print(f"2000th = {L[(zero + 2000)% len(L)]}")
    print(f"3000th = {L[(zero + 3000)% len(L)]}")

    r = L[(zero + 1000)% len(L)] + L[(zero + 2000)% len(L)] + L[(zero + 3000)% len(L)]
    print(f"Result is {r}")
    return r


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
        L.append(int(l))
        I.append(lcount -1)

# print("SOURCE:")
# print(f"L = {L}")
# print("")
for i in range(len(L)):
    #at what position of I is the nth number we should process
    pos = -1
    for j in range(len(I)):
        if I[j] == i:
            pos = j
            break

    if DBG:
        print(f"== Processing turn {i}  ==")
        print(f"L = {L}\nI = {I}")
    rotate(pos)
    if DBG:
        print(f"L = {L}")
        print(f"I = {I}")
        print("\n")

    # if i == 100:
    #     print("DEBUG STOP")
    #     break

calcResult()