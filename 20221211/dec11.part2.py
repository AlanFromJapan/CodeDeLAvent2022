import io
import sys

monkeysDict = {}

class Monkey():
    id = 0
    items=[]
    operation = ""
    testDivider = 0
    testIfTrueMonkey = 0
    testIfFalseMonkey = 0
    processedItemsCount = 0

    def __init__(self, id, items, operation, testDivider, testTrue, testFalse) -> None:
        self.id = id
        self.items = [int(x) for x in items] #my first python lambda :'D
        self.operation = operation
        self.testDivider = testDivider
        self.testIfTrueMonkey = testTrue
        self.testIfFalseMonkey = testFalse
        self.processedItemsCount = 0

    def calculateNewWorry(self, n):
        # formula = self.operation.replace("old", str(n))
        # return int(eval(formula))
        formula = self.operation.split(" ")
        if formula[0] == "old":
            formula[0] = n
        if formula[2] == "old":
            formula[2] = n
        
        if formula[1] == "+":
            return int(formula[0]) + int(formula[2])
        else:
            return int(formula[0]) * int(formula[2])

    def giveItem(self, worry):
        self.items.append(worry)

    def takeTurn(self):
        if len(self.items) == 0:
            print(f"Monkey {self.id} has nothing to do.")
        else:
            print(f"Monkey {self.id} will process {len(self.items)}")

            for i in self.items:
                #print(f"  Monkey inspects an item with a worry level of {i}.")
                #newWorry = self.calculateNewWorry(i)
                #print(f"    Worry level is {self.operation} to {newWorry}.")
                #newWorry = int(newWorry / 3)
                #print(f"    Monkey gets bored with item. Worry level is divided by 3 to {newWorry}.")

                formula = self.operation.split(" ")
                if formula[2] == "old":
                    formula[2] = i
        
                #Modulo arithmetic is all we care and seems distribuable in integer space
                #https://en.wikipedia.org/wiki/Modular_arithmetic#Integers_modulo_n
                mod = False
                if formula[1] == "+":
                    mod = ((i % self.testDivider) + (int(formula[2]) % self.testDivider)) % self.testDivider
                else:
                    mod = (i % self.testDivider) * (int(formula[2]) % self.testDivider)

                if mod == 0:
                    #print(f"    Current worry level is divisible by {self.testDivider}.")

                    #print(f"    Item with worry level {newWorry} is thrown to monkey {self.testIfTrueMonkey}.")
                    monkeysDict[self.testIfTrueMonkey].giveItem (i)
                else:
                    #print(f"    Current worry level is not divisible by {self.testDivider}.")

                    #print(f"    Item with worry level {newWorry} is thrown to monkey {self.testIfFalseMonkey}.")
                    monkeysDict[self.testIfFalseMonkey].giveItem (i)
                
                #keep track
                self.processedItemsCount = self.processedItemsCount + 1

            #finished processing all, list is empty
            self.items = []


    def __str__(self) -> str:
        return "Monkey %d : items %s, Ops '%s', Mod %d  ~~ Processed %d items." % (self.id, self.items, self.operation, self.testDivider, self.processedItemsCount)


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
        if l.startswith("Monkey"):
            id = int(l.split(" ")[1][:-1])
            
            l = f.readline().strip()
            items = l[len("Starting items:"):].strip().split(", ")

            l = f.readline().strip()
            ops = l[len("Operation: new = "):]

            l = f.readline().strip()
            test = int(l[len("Test: divisible by "):])

            l = f.readline().strip()
            testT = int(l[len("If true: throw to monkey "):])

            l = f.readline().strip()
            testF = int(l[len("If false: throw to monkey "):])

            m = Monkey(id, items, ops, test, testT, testF)
            monkeysDict[m.id] = m

for m in monkeysDict.values():
    print(m)

print ("-------------------- START --------------------------")

maxTurns = 10000
for turn in range(maxTurns):
    print(f">>>>> Turn {turn}")

    for mi in range(len(monkeysDict)):
        #to be sure we go in right order
        m = monkeysDict[mi]
        m.takeTurn()
    
    print(f"<<<<<< END OF TURN {turn}")
    # for m in monkeysDict.values():
    #     print(m)


for m in monkeysDict.values():
    print(m)

processed = []
for m in monkeysDict.values():
    processed.append(m.processedItemsCount)

max1 = max(processed)
processed.remove(max1)
max2 = max(processed)
print (f"Maxes are {max1:,} x {max2:,} = {max1 * max2:,}")