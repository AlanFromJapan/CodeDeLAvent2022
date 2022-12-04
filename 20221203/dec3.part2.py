import io

def commonChars (a, b, z):
    result = []
    for c in a:
        if c in b and c in z and not c in result:
            result.append(c)
    return result

def char2points(c):
    if c >= 'a' and c <='z':
        return 1 + ord(c) - ord('a')
    else:
        #assume A-Z
        return 26 + 1 + ord(c) - ord('A')

def sumForPeopleWhoDontGetLambdas (li):
    acc = 0
    for c in li:
        acc = acc + char2points(c)
    return acc


lcount = 0
total = 0
grandtotal = []
trio = []
with io.open("input.txt", "r") as f:
    while True:
        l = f.readline()
        lcount = lcount +1

        if not l:
            #finished!
            break

        # if lcount > 50:
        #     break

        #process!
        l = l.strip()

        trio.append(l)

        if len(trio) < 3:
            continue
        else:
            #3 items, process
            matches = commonChars (trio[0], trio[1], trio[2])
            matchesVal = sumForPeopleWhoDontGetLambdas(matches)
            grandtotal.append(matchesVal)

            #print ("> %s (%d) vs %s (%d) : %s = %d" % (compartments[0], len(compartments[0]), compartments[1], len(compartments[1]), matches, matchesVal))
            print("> %s = %d" % (matches, matchesVal))

            #DON'T FORGET TO RESET
            trio.clear()

print ("Grand total: " + str(sum(grandtotal)))


