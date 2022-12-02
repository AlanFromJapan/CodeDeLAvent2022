#https://adventofcode.com/2022/day/2

#A for Rock, B for Paper, and C for Scissors
#!!!!!
#X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
#1 for Rock, 2 for Paper, and 3 for Scissors
#0 if you lost, 3 if the round was a draw, and 6 if you won

import io

pointsPerType = {"X" : 1, "Y" : 2, "Z" : 3}
RES_WIN = 6
RES_DRAW = 3
RES_LOSS = 0

#Maps they to me depending on goal
toWin = {"A" : "Y", "B": "Z", "C": "X"}
toLose = {"A" : "Z", "B": "X", "C": "Y"}
toDraw = {"A" : "X", "B": "Y", "C": "Z"}


#returns how many points won this turn
def calcWinLoss (they, me):
    #me is X=lose, Y=draw, Z=win
    mypick = ""
    if me == "X":
        mypick = toLose[they]
    elif me == "Z":
        mypick = toWin[they]
    else:
        mypick = toDraw[they]
    
    if mypick + they in ("XA", "YB", "ZC"):
        return pointsPerType[mypick] + RES_DRAW
    if mypick + they in ("XC", "YA", "ZB"):
        return pointsPerType[mypick] + RES_WIN
    if mypick + they in ("XB", "YC", "ZA"):
        return pointsPerType[mypick] + RES_LOSS

lcount = 0
total = 0
with io.open("input.txt", "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if lcount > 50:
        #     break

        round = l.strip().split(" ")
        print("Round "+ str(lcount) + ": " + str(round) + " > " + str(calcWinLoss(round[0], round[1])))
        
        total = total + calcWinLoss(round[0], round[1])

print ("GRAND TOTAL: " + str(total))
