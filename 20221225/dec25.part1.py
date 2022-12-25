import io
import sys

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


#convert a number from base 10 to base n
def dec2basen(num, base):
    res = ""

    while num > 0:
        res = str(num % base) + res

        num = num // base

    return res

def prettyPrintDec2N (num, base):
    print(f"Convert {num} (base 10) to '{dec2basen(num, base)}' (base {base})")


#convert a number from  base n to base 10
def basen2dec(num, base):
    res = 0

    b = 1
    while num != '':
        #print(f"r {res} n {num}")
        res = int(str(num)[-1]) * b + res
        num = str(num)[:-1]
        b = b * base

    return res

def prettyPrintN2Dec (num, base):
    print(f"Convert {num} (base {base}) to '{basen2dec(num, base)}' (base 10)")


prettyPrintN2Dec(1, 2)
prettyPrintN2Dec(10, 2)
prettyPrintN2Dec(100, 2)
prettyPrintN2Dec(101, 2)
prettyPrintN2Dec(1111, 2)
prettyPrintN2Dec(10000, 2)
prettyPrintN2Dec(111111, 2)

prettyPrintN2Dec(1, 5)
prettyPrintN2Dec(2, 5)
prettyPrintN2Dec(3, 5)
prettyPrintN2Dec(12, 5)
prettyPrintN2Dec(30, 5)
prettyPrintN2Dec(31, 5)
prettyPrintN2Dec(223, 5)

print("***************************************** ")
prettyPrintDec2N(1, 2)
prettyPrintDec2N(2, 2)
prettyPrintDec2N(3, 2)
prettyPrintDec2N(8, 2)
prettyPrintDec2N(10, 2)
prettyPrintDec2N(15, 2)
prettyPrintDec2N(16, 2)
prettyPrintDec2N(63, 2)

prettyPrintDec2N(1, 5)
prettyPrintDec2N(2, 5)
prettyPrintDec2N(3, 5)
prettyPrintDec2N(8, 5)
prettyPrintDec2N(10, 5)
prettyPrintDec2N(15, 5)
prettyPrintDec2N(16, 5)
prettyPrintDec2N(63, 5)

exit()

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

