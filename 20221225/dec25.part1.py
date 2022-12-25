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

SNAFU = ["2", "1", "0", "-", "="]
def base5toSnafu (n):
    #assume input in base 5 already
    #it should be like coding roman numbers, can be done with a carry like propagation
    res = ""
    n = str(n)
    carry= 0

    while len(n) > 0:
        #digit is [0 - 6] (6 because max 4 + 2 carry)
        digit = int(n[-1]) + carry
        #print(f"  * digit {digit} = {n[-1]} + carry {carry}")
        
        nextCarry = 0
        if digit > 4:
            nextCarry = nextCarry + 1
            digit = digit - 5
        
        if digit<= 2:
            #nothing to do
            res = str(digit) + res
        elif digit == 3:
            nextCarry = nextCarry +1
            res = "=" + res
        elif digit == 4:
            nextCarry = nextCarry +1
            res = "-" + res

        carry = nextCarry

        n = n[:-1]

    if carry != 0:
        res = str(carry) + res

    return res

def prettyPrintN2Snafu (num, base):
    print(f"Convert {num} (base {base}) to '{base5toSnafu(dec2basen(basen2dec(num, base), 5))}' (base snafu)")

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
        #l = l.strip()

        #edit me v v v v v  
        #print(f"{lcount}: {l}") 
        ll = [l[:10].strip(), l[11:].strip()]
        #print(ll)
        prettyPrintN2Snafu(int(ll[0]), 10)
        print(f"   Expects {ll[0]} -> {ll[1]}")
