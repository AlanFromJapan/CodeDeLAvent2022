import io


class Fichier():
    name = ""
    parent = None
    size = 0

    def __init__ (self, name, parent):
        self.name = name
        self.parent = parent
        if not isinstance(self, Repertoire) and not self.parent == None:
            self.parent.files.append(self)

    def getSize(self):
        return self.size

    def __str__(self):
        return self.name + " " + str(self.size)



class Repertoire(Fichier):
    subfolders = []
    files = []

    
    def __init__ (self, name, parent):
        Fichier.__init__(self, name, parent)
        self.subfolders = []
        self.files = []
        if not self.parent == None:
            self.parent.subfolders.append(self)

    def getSize(self):
        t = 0
        for f in self.files:
            t = t + f.getSize()
        for s in self.subfolders:
            t = t + s.getSize()
        return t

    def __str__(self):
        res = "+ " + self.name
        for s in self.subfolders:
            res = res + "\n" + str(s)
        for f in self.files:
            res = res + "\n" + str(f)
        return res

    def show(self, n=0,showFiles=True):
        spacer = "  " * n
        print (F"{spacer}Dir: {self.name} [{self.getSize():0,}]")
        if showFiles:
            for f in self.files:
                print(f"{spacer} - {f.name} {f.size:0,}")
        for s in self.subfolders:
            s.show(n+1, showFiles)

    def filterMax(self, maxVal):
        t = 0
        res = []
        for f in self.files:
            t = t + f.getSize()
        for s in self.subfolders:
            t = t + s.getSize()
        
        if t <= maxVal:
            res.append(t)
        
        for s in self.subfolders:
            subRes = s.filterMax(maxVal)
            if not subRes == []:
                #+= combines 2 list, append() would nest them
                res += subRes 
        
        return res
        

    def smallestFolderBiggerThan (self, missing):
        sz = self.getSize()
        #end of recc
        if len(self.subfolders) == 0:
            #return sz if sz > missing else 0
            x = sz if sz > missing else 0
            #print (f"Leaf '{self.name}' : {sz} => {x}")
            return x

        #rec
        l = []
        for s in self.subfolders:
            l.append(s.smallestFolderBiggerThan(missing))
        #self
        if sz > missing:
            l.append(sz)

        #return the min that is above missing
        l_without_0 = [x for x in l if x != 0]
        x = min(l_without_0) if len(l_without_0) > 0 else 0
        #print (f"Rec '{self.name}' : {l_without_0} => {x}")
        return x



lcount = 0
root = Repertoire("/", None)
current = root
with io.open("input.txt", "r") as f:

    #this script only, trash line 1 "cd /" that makes the code unnecessarily complex
    l = f.readline()

    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if lcount > 200:
        #     break

        #process!
        l = l.strip()

        if l[0] == "$":
            #command mode
            cmd = l[2:].split(" ")
            #print (cmd)

            #ls?
            #do nothing, it's the else case and we just add to current folder

            #cd
            if cmd[0] == "cd":
                if cmd[1] == "..":
                    #print(f"> Up one folder from {current.name} to {current.parent.name}")
                    current = current.parent
                else:
                    #go to a subfolder
                    #ASSUME it'S first time, no back track so just bluntly create
                    #print("> Move from " + current.name + " to " + cmd[1])

                    d = Repertoire(cmd[1], current)
                    current = d
        else:
            #folder enum
            content = l.split(" ")
            if content[0] == "dir":
                #ignore, we'll list when visit
                pass
            else:
                sz = int(content[0])
                nm = content[1]
                fi = Fichier(nm, current)
                fi.size = sz


root.show(showFiles=False)
rootSz = root.getSize()
print (f"size = {rootSz:0,}")
TOTALDISK=70000000
NEED=30000000
missing = TOTALDISK - rootSz
print(f"Missing {missing:0,} bytes")
print(f"Minimum freeable space is {root.smallestFolderBiggerThan(missing):0,}")