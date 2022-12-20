import io
import sys

filename = "input.txt"
llimit = -1

#the current list of numbers 
L = []
#by index where they were in the ORIGINAL data
I = []

#Rotate both the values L and index I according the I[ipos]
def rotate(ipos):
    global L, I
    lpos = ipos
    val = L[lpos]

    offset = val % len(L)
    if val < 0:
        offset = offset - 1

    print(f">> ipos={ipos}, lpos={lpos}, val={val}")

    #remove value
    L = L[:lpos] + L[lpos+1:]
    I = I[:ipos] + I[ipos+1:]

    #insert value (don't care of original pos anymore hence -1)
    L= L[:lpos + offset] + [val] + L[lpos + offset:]
    I= I[:ipos + offset] + [-1] + I[ipos + offset:]

    

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

for i in range(len(L)):
    #at what position of I is the nth number we should process
    pos = -1
    for j in range(len(I)):
        if I[j] == i:
            pos = j
            break

    print(f"== Processing turn {i}  ==")
    #print(f"L = {L}\nI = {I}")
    rotate(pos)
    print(f"L = {L}")
    #print(f"I = {I}")
    print("\n")

    if i == 100:
        break
