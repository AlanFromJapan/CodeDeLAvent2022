#https://adventofcode.com/2022/day/2

#A for Rock, B for Paper, and C for Scissors
#X for Rock, Y for Paper, and Z for Scissors
#1 for Rock, 2 for Paper, and 3 for Scissors
#0 if you lost, 3 if the round was a draw, and 6 if you won

import io

pointsPerType = {"X" : 1, "Y" : 2, "Z" : 3}
RES_WIN = 6
RES_DRAW = 3
RES_LOSS = 0

#returns how many points won this turn
def calcWinLoss (they, me):
    res = 0
    if me + they in ("XA", "YB", "ZC"):
        return pointsPerType[me] + RES_DRAW
    if me + they in ("XC", "YA", "ZB"):
        return pointsPerType[me] + RES_WIN
    if me + they in ("XB", "YC", "ZA"):
        return pointsPerType[me] + RES_LOSS

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
