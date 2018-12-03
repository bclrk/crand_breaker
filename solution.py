import random
import copy

def crand(seed):
    r=[]
    r.append(seed)
    for i in range(30):
        r.append((16807*r[-1]) % 2147483647)
        if r[-1] < 0:
            r[-1] += 2147483647
    for i in range(31, 34):
        r.append(r[len(r)-31])
    for i in range(34, 344):
        r.append((r[len(r)-31] + r[len(r)-3]) % 2**32)
    while True:
        # line below was: next = r[len(r)-31]+r[len(r)-3] % 2**32
        next = (r[len(r)-31]+r[len(r)-3]) % 2**32
        r.append(next)
        yield (next >> 1 if next < 2**32 else (next - 2**32) >> 1)

theseed = random.randint(1, 2**30)
skip = random.randint(10000, 200000)
print "theseed", theseed
print "skip", skip, "\n"

my_generator = crand(theseed)
for i in range(skip):
    temp = my_generator.next()

the_input = [my_generator.next() for i in range(100)] # was range(80)

the_output = [my_generator.next() for i in range(100)] # was range(80)


def r2o(ris, n):
    ''' convert r_i to o_i for 1<= i < n'''
    ois = []
    for _ in range(n):
        temp = (ris[0]+ris[28]) % 2**32
        ris = ris[1:]
        ris.append(temp)
        ois.append(temp >> 1)
    return ois

def find_ris(theinput):
    l = len(theinput)
    # (o_i, r_i, certainty); may need to add 1 to r_i; certainty=True when we
    # know r_i is correct
    values = [[theinput[i], theinput[i]<<1, False] for i in range(l)]
    for i in range(31, l):
        potential_oi = ( (values[i-31][1]+values[i-3][1])%2**32 ) >> 1
        if potential_oi == values[i][0]: # could still add 1 and this be true
            # certain and we've added 1
            if values[i-31][2] and (values[i-31][1]==(values[i-31][0]<<1)+1):
                values[i-3][2] = True
        elif (potential_oi + 1) == values[i][0]: # r_i's need 1, for sure
            # only if not already correct
            if not values[i-31][2]:
                values[i-31][1] += 1
                values[i-31][2] = True
            if not values[i-3][2]:
                values[i-3][1] += 1
                values[i-3][2] = True
                
    # --------------- above significantly narrows search space ---------------
    # --------------- below we will check all other combinations -------------
    
    # (running the commented-out parts will be faster but not always correct)
    # searchSpace = [values[i][2] for i in range(l-31-31,l-31)].count(False)
    searchSpace = [values[i][2] for i in range(31)].count(False)
    print "searchSpace", searchSpace
    for a in range(2**searchSpace):
        # editValues = copy.deepcopy(values[l-31-31:])
        editValues = copy.deepcopy(values)
        m2s = [int(e) for e in str(bin(a))[2:].zfill(searchSpace)]
        index2s = 0
        for i in range(31):
            if not editValues[i][2]:
                editValues[i][1] += m2s[index2s]
                index2s += 1
        # if r2o([editValues[i][1] for i in range(31)], 31) == theinput[-31:]:
        if r2o([editValues[i][1] for i in range(31)], l-31) == theinput[31:]:
            return [editValues[i][1] for i in range(31)]

    for i in range(31):
        if not values[i][2]:
            print "WARNING - value at", i, "is uncertain"
    return [values[i][1] for i in range(31)]

def your_code(theinput):
    ''' given l values, return the next l '''
    l = len(theinput)
    # this is the correct r_{l-31-31}:r_{l-31}
    ris = find_ris(theinput)
    # we need r_{l-31}:r_{l-1}
    # ois = r2o(ris, l+31) # for the less accuracy faster way
    # return ois[31:] # for the less accuracy faster way
    ois = r2o(ris, 2*l-31)
    return ois[l-31:]

myoutput = your_code(the_input)
if myoutput == the_output:
    print "You win"
else:
    print "Try again"
