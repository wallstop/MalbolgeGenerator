# @Author: Eli Pinkerton
# @Description: A mostly-complete collection of useful malbolge methods

# To run a malbolge program, call feedInstruction(malbolgeString)

# To run a malbolge program that is in terms of opCodes, call interpret(malbolgeString)

# To generate a malbolge program that prints a desired string, call findString(desiredString)

import math

# Translation tables used for deciphering/enciphering code
normalTranslate =     '+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z\';FNQuY]szf$!BS/|t:Pn6^Ha'
encryptionTranslate = '5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK\'X~xDl}REokN:#?G\"i@'
validInstructions = "i</*jpov"

# Global variables that represent the current state of the malbolge tape and registers
malbolgeTape = list()
a = 0
c = 0
d = 0

# Converts ASCII-representation to Malbolge-style instructions
def normalize(instructionList):
    global validInstructions
    global normalTranslate
    returnString = ''

    # Checks for valid program length
    if(len(instructionList) > 59049):
        print("Excessive program length")
        return
    # Convert the code character by character
    for x in range(0, len(instructionList)):
        tempChar = normalTranslate[((ord(instructionList[x]) + x - 33) % 94)]
        if tempChar in validInstructions:
            returnString += tempChar

    return list(returnString)

# Converts from Malbolge-style instructions to actual ASCII-representation
def reverseNormalize(instructionList):
    global validInstructions
    global normalTranslate
    returnString = ''

    # Check for a valid program length
    if(len(instructionList) > 59049):
        print("Excessive program length")
        return

    # Convert the code character by character
    for x in range(0, len(instructionList)):
        #Checks to see if the instructions provided are valid
        if instructionList[x] in validInstructions:
            tempChar = chr(((normalTranslate.index(instructionList[x]) - x) % 94) + 33)
            returnString += tempChar
        else:
            print("Invalid program string.")
            return

    return list(returnString)

# Converts from base10 to base3
def convertToBase3(inputInteger):
    ternaryList = list()

    # Base converstion
    while(inputInteger):
        ternaryList.append(inputInteger % 3)
        inputInteger = math.floor(inputInteger / 3)

    # Fills missing "memory" cells (Malbolge requires 10)
    while(len(ternaryList) < 10):
        ternaryList.append(0)
    

    return ternaryList


# Converts from base3 to base10
def convertToBase10(ternaryList):
    returnInt = 0
    for x in range(0, len(ternaryList)):
        returnInt += ternaryList[x] * int(math.pow(3, x))

    return returnInt
    

# Converts a base 10 number to base 3, rotates one bit, and converts back
def ternaryRotate(inputInteger):
    
    ternaryList = convertToBase3(inputInteger)

    # Performs the rotate
    ternaryList.append(ternaryList[0])
    ternaryList.pop(0)

    return convertToBase10(ternaryList)

# Performs the crazy operation on two numbers
def crazyOperation(first, second):

    firstList = convertToBase3(first)
    secondList = convertToBase3(second)
    
    # Creates a list of length 10, we don't care what's in it
    thirdList = list(range(10))

    # This could probably be better done using a table and just indexing into it, but, oh well
    for x in range(0, len(thirdList)):
        if(firstList[x] == 0 and (secondList[x] == 0 or secondList[x] == 1)):
            thirdList[x] = 1
        elif((firstList[x] == 0 or firstList[x] == 1) and secondList[x] == 2):
            thirdList[x] = 2
        elif((firstList[x] == 1 or firstList[x] == 2) and secondList[x] == 0):
            thirdList[x] = 0
        elif(firstList[x] == 1 and secondList[x] == 1):
            thirdList[x] = 0
        elif(firstList[x] == 2 and secondList[x] == 1):
            thirdList[x] = 2
        elif(firstList[x] == 2 and secondList[x] == 2):
            thirdList[x] = 1

    return convertToBase10(thirdList)

# Determines the instruction to execute
def getInstruction():
    global malbolgeTape
    global normalTranslate
    global c
    
    return normalTranslate[(malbolgeTape[c] - 33 + c) % 94]

# Used to encrypt positions on the tape after the instruction there is executed
def encrypt():
    global malbolgeTape
    global encryptionTranslate
    global c

    if(33 <= malbolgeTape[c] and malbolgeTape[c] <= 126):
        malbolgeTape[c] = ord(encryptionTranslate[malbolgeTape[c] - 33])

# Given an opCode representation of a malbolge program, runs it
def interpret(instructionList):
    global validInstructions
    global normalTranslate
    global encryptionTranslate
    global malbolgeTape
    global a
    global c
    global d

    running = True
    outputString = ""
    maxInstructions = len(instructionList)

    # Registers
    a = 0
    c = 0
    d = 0

    # Determines the actual malbolge code, and assigns it to the malbolgeTape
    malbolgeTape = reverseNormalize(instructionList)

    # Converts the characters on the tape to their numerical values
    for x in range(0, len(malbolgeTape)):
        malbolgeTape[x] = ord(malbolgeTape[x])

    # Used to "properly" initialize the malbolgeTape. However, this is a huge performance hit, as most malbolge programs are significantly less than the maximum size, and the crazy ops take time to calculate
    # So, instead, I've added some checks into the interpreter to simply exit on invalid tape indexes. The below section should be uncommented if you wish for "proper" machine execution
    
    #currentIndex = len(malbolgeTape)    
    #while(currentIndex < 59049):
    #    malbolgeTape.append(crazyOperation(malbolgeTape[currentIndex - 2], malbolgeTape[currentIndex - 1]))
    #    currentIndex += 1

    
    while(running):
        currentInstruction = getInstruction()

        # Executes instructions
        if(currentInstruction == 'i'):
            if(d >= maxInstructions):
                running = False
                break
            c = malbolgeTape[d]
        elif(currentInstruction == '<'):
            outputString += chr(a % 256)
        elif(currentInstruction == '/'):
            a = input()     # Pretend user input is valid
        elif(currentInstruction == '*'):
            if(d >= maxInstructions):
                running = False
                break
            a = ternaryRotate(malbolgeTape[d])
            malbolgeTape[d] = a
        elif(currentInstruction == 'j'):
            if(d >= maxInstructions):
                running = False
                break
            d = malbolgeTape[d]
        elif(currentInstruction == 'p'):
            if(d >= maxInstructions):
                running = False
                break
            a = crazyOperation(a, malbolgeTape[d])
            malbolgeTape[d] = a
        elif(currentInstruction == 'v'):
            running = False

        # Encrypts the last-executed instructions on the tape
        # If you aren't using jumps, this isn't technically necessary
        encrypt()

        # Auto-increment C and D
        c += 1
        if(c >= maxInstructions):
            running = False
        d += 1


    return outputString

# Given a malbolge program, interprets it
def feedInstructions(inputString):
    return interpret(normalize(inputString))

# Given an opCode representation of a malbolge program, prints out the actual malbolge code that corresponds to it
def printMalbolgeProgram(inputString):
    outputString = reverseNormalize(inputString)
    for x in outputString:
        print(x, end='')
    print()

# The actual generation method
# Generates a malbolge program that prints the desired string
def findString(inputString):
    global malbolgeTape
    
    from random import choice

    # This is the  list of opcodes that the program will use (aside from <)
    # p and * change the value of A, which is crucial for printing
    # o is nice to have, because it increments D, which is then used to get different values of A through * and p
    # j can also be used here, but might crash the program (not sure if I handle jumps to places without data)
    opCodes = "op*"

    # endString holds the currently-found Malbolge program, in terms of operations
    endString = ""

    # Master loop, looks for letters
    for x in range(0, len(inputString)):

        tempString = ""
        
        # Whether or not the current letter of the desired string has been found
        found = False

        # masterList holds all possible combination of the above opCodes for some length.
        masterList = list()

        # tempList is used as a temporary holder while all possible combinations of opCodes of length + 1 are generated
        tempList = list()

        # Tries only a single opcode at first, length of masterList is 1
        for y in opCodes:
            masterList.append(y)

        # Counter is used to keep track of iterations while searching
        counter = 0
        
        while not found:
            counter += 1

            # Iterates through all possible combinations of opcodes for the current length, and sees if any of them print the desired character
            for y in masterList:
                tempString = interpret(endString + y + "<")

                # If the desired character is found, then that means that the current malbolge program prints out inputString up until the character we're searching for
                # Alternatively, we could compare the last letter of the malbolge program, but if we were using actual jumps, it might be possible that the output has become corrupted
                #   So just in case, we do a substring comparison
                if(tempString == inputString[:(x + 1)]):
                    endString += y + "<"
                    found = True
                    break
                
            # Clear templist of previous results
            tempList = list()

            # Only mess around with masterList and tempList if we haven't found a solution. 
            if not found:
                for y in masterList:
                    # Generate all possible combinations of length + 1
                    for z in opCodes:
                        tempList.append(y + z)
                        
                # Update masterList with these new combinations (clears all old ones)
                masterList = tempList

            # This is the novel part. If no solution has been found by length 5, a random combination of opCodes is appended to the current-good malbolge program.
            # The rational behind this is that most combinations of the above opcodes will change the value of A. With enough changes, eventually A will have a value that allows some combination of 5 opcodes to reach the desired character
            # This potentially makes the code run infinitely, but the likelyhood of this is infinitismally small.
            if(counter == 5 and not found):
                endString += choice(masterList)

                # Reset opCode combinations
                masterList = list()
                for y in opCodes:
                    masterList.append(y)
                counter = 0

        # Used to visualize where the malbolge program currently is in inputString
        print(inputString[x], end='')

    print()

    # Prints the actual malbolge code
    printMalbolgeProgram(endString + "v")

    # Returns the opcodes
    return endString + "v"
