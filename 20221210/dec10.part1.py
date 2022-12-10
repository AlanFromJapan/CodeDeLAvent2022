import io
import sys

class CPU:
    tick = 1
    X = 1
    history = []

    def __init__(self) -> None:
        self.tick = 1
        self.X = 1
        self.history = []

    def saveHistory(self, cmd=""):
        self.history.append([self.tick, self.X, cmd])

    def noop(self):
        self.tick = self.tick +1
        self.saveHistory("noop")

    def addx(self, v):
        self.tick = self.tick +1
        self.saveHistory()        
        self.tick = self.tick +1
        self.X = self.X + v
        self.saveHistory("addx " + str(v))

    def showHistory(self):
        for h in self.history:
            print(f"{h[0]:000000} : X={h[1]}{' -> ' + h[2] if not h[2] == '' else ''}")

    def calculateResult(self):
        total = 0
        moments =[20, 60, 100, 140, 180, 220]
        for h in self.history:
            if h[0] in moments:
                total = total + int(h[0]) * int(h[1])
        return total


cpu = CPU()
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
        if l == "noop":
            cpu.noop()
        else:
            cmd = l.split(" ")
            if cmd[0] == "addx":
                cpu.addx(int(cmd[1]))
        

cpu.showHistory()
print (f"Total is {cpu.calculateResult()}")