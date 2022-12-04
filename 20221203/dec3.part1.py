import io

def commonChars (a, b):
    result = []
    for c in a:
        if c in b and not c in result:
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
        compartments = []
        compartments.append(l[:int(len(l)/2)])
        compartments.append(l[int(len(l)/2):])

        matches = commonChars(compartments[0], compartments[1])
        matchesVal = sumForPeopleWhoDontGetLambdas(matches)
        grandtotal.append(matchesVal)
        #print ("> %s (%d) vs %s (%d) : %s = %d" % (compartments[0], len(compartments[0]), compartments[1], len(compartments[1]), matches, matchesVal))

print ("Grand total: " + str(sum(grandtotal)))


