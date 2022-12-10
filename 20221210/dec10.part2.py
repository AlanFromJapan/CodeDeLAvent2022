import io
import sys

class CPU:
    tick = 1
    X = 1
    history = []
    display = None

    def __init__(self) -> None:
        self.tick = 1
        self.X = 1
        self.history = []
        self.display = None

    def doTick(self):
        self.tick = self.tick +1
        self.display.doTick()

    def saveHistory(self, cmd=""):
        self.history.append([self.tick, self.X, cmd])

    def noop(self):
        self.doTick()
        self.saveHistory("noop")

    def addx(self, v):
        self.doTick()
        self.saveHistory()        
        self.doTick()
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
    
    def linkDisplay(self, display):
        #yes circular reference I know :P
        self.display = display

class Display():
    rows = []
    ROW_COUNT=6
    PIXEL_PER_ROW=40
    PIXEL_OFF="."
    PIXEL_ON="#"
    cpu = None

    currentPixel=[0,0]

    def __init__(self, cpu: CPU) -> None:
        self.rows = []
        self.currentPixel = [0,0]

        self.cpu = cpu
        cpu.linkDisplay(self)

        for i in range(self.ROW_COUNT):
            self.rows.append(Display.PIXEL_OFF * Display.PIXEL_PER_ROW)

    def show(self):
        for ro in self.rows:
            print(f"[{ro}]")
    
    def doTick(self):
        val = Display.PIXEL_ON if abs(cpu.X - self.currentPixel[0]) <= 1 else Display.PIXEL_OFF

        #string are immutable...
        x = self.currentPixel[0]
        ro = self.rows[self.currentPixel[1]]
        self.rows[self.currentPixel[1]] = ro[:x] + val + ro[x+1:]
        
        #move to next pixel
        self.currentPixel[0] = self.currentPixel[0] + 1
        if self.currentPixel[0] >= Display.PIXEL_PER_ROW:
            self.currentPixel[0] = 0
            self.currentPixel[1] = self.currentPixel[1] +1
        if self.currentPixel[1] >= Display.ROW_COUNT:
            self.currentPixel[1] = 0


cpu = CPU()
display=Display(cpu=cpu)
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
        

#cpu.showHistory()
#print (f"Total is {cpu.calculateResult()}")
print("Output:")
display.show()