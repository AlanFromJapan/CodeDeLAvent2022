import io

#returns N tops of a list L
def getNmaxes(l, n):
    res = []
    for i in range(n):
        res.append(max(l))
        l.remove(max(l))
    return res

dictResult = {}
elfId = 0
lcount = 0

with io.open("input.txt", "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break
        #print ("> line " + str(lcount))

        # if lcount > 20:
        #     break

        #change of elf
        if l.strip() == "":
            #new elf
            #print("New elf!")
            elfId = elfId + 1
        else:
            #add
            #print("Add to " + str(elfId))
            dictResult[elfId] = int(l) + (0 if not elfId in dictResult else dictResult[elfId])

#print (dictResult)
print ("Max is "+ str(max(list(dictResult.values()))))
top4 = getNmaxes(list(dictResult.values()), 4)
print ("Top 4 are " + str(top4))
print ("Sum of top 3 = " + str(top4[0] + top4[1] + top4[2]))