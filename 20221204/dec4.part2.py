import io

#returns if a is fully contained in b, or the opposite
def fullyContains(a,b):
    #need int conversion or some string conversion hapen and detects "2-6,13-87" as overlap for instance :/
    return (int(a[0]) >= int(b[0]) and int(a[1]) <= int(b[1])) or (int(b[0]) >= int(a[0]) and int(b[1]) <= int(a[1]))

def justOverlap (a,b):
    #trick is the say non total exclusion
    return not ( int(a[0]) > int(b[1]) or  int(b[0]) > int(a[1])  )

lcount = 0
grandTotal = 0
with io.open("input.txt", "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if lcount > 10:
        #     break

        #process!
        l = l.strip()
        assignment = l.split(",")
        elf1 = assignment[0].split("-")
        elf2 = assignment[1].split("-")

        #print ("? %s %s " % (elf1, elf2))
        if justOverlap(elf1, elf2):
            print (">> %s overlap" % (l))
            grandTotal = grandTotal + 1

print ("Grand Total: %d" % (grandTotal))
