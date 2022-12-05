import io

def initTowers():
    t = []
    for i in range(9):
        t.append([])
    return t


def parseInitialStatus(l, towers):
    #jsut read at exepcted index if there's enough data
    for i in range (9):
        idx = 2 + i* 4 -1
        if len(l) > (idx +1):
            c = l[idx]
            if not c == " " and (ord(c) >= ord("A") and ord(c) <= ord("Z")):
                towers[i].append(c)
    return towers

lcount = 0
towers = initTowers()
phase = 1
with io.open("input.txt", "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if lcount > 20:
        #     break

        #process!
        #DO NOT strip for 1st phase! l = l.strip()
        if phase == 1:
            #reading the initial status
            print(f"> reading line {lcount}")
            towers = parseInitialStatus(l, towers)

            if l.strip() == "":
                #finisehd parsing initial status
                print("Initial status")
                print(towers)
                print(" ")
                phase = 2
                continue
        
        #parsing the moves
        if phase == 2:
            l = l.strip()
            if l == "":
                break
            words = l.split(" ")

            qty = int(words[1])
            src = int(words[3]) -1
            dst = int(words[5]) -1

            #remove the crates
            crates = towers[src][:qty]
            towers[src] = towers[src][qty:]

            # print(l)
            # print(crates)

            #add the crates (on top), and since moved "1by1" need to reverse the list
            crates.reverse()                
            crates.extend(towers[dst])
            towers[dst] = crates

            # print(towers)
            #break

print("Final status")
print (towers)

secret = ""
for i in range(9):
    secret = secret + towers[i][0]
print (f"Secret: {secret}")