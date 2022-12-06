import io

def hasDup(msg):
    dic = {}
    for c in msg:
        dic[c] = c

    return not (len(dic) == len(msg))

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
        msg = ""
        pos = 0
        for c in l:
            pos = pos+1
            msg = msg + c
            if len(msg) < 14:
                continue
            
            #print("> " + msg)
            if not hasDup(msg):
                print(f"Found at {pos}!")
                break

            #drop 1st char
            msg = msg[1:]

            # if pos > 20:
            #     break    