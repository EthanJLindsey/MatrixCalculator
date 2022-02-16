import os.path
import time
 
# inputs two nested lists where each element in each matrix is one row
def matrixMult(matrix1, matrix2):
    if len(matrix1[0])!=len(matrix2):
        print("Incompatible matrices!")
        return
    result = []
    for i in range(0,len(matrix1)):
        result.append([])
        for j in range(0,len(matrix2[0])):
            element = 0.0
            for k in range(0,len(matrix2)):
                element += matrix1[i][k]*matrix2[k][j]
            result[i].append(element)
    return result

#prompts input for new matrix
def newMatrix():
    done = False
    while not done:
        numRows = safeInput("How many rows does your matrix have?",
                        "The number of rows needs to be an integer.",int)
        numColumns = safeInput("How many columns does your matrix have?",
                        "The number of columns needs to be an integer.",int)
        matrix = []
        for i in range(0,numRows):
            matrix.append([])
            for j in range(0,numColumns):
                matrix[i].append(safeInput("Row "+str(i+1)+" and Column "+str(j+1)+"? ",
                            "Input must be a decimal. No fractions are allowed.",float))
        print("New Matrix Created:")
        print(matrixToString(matrix))
        done = promptYesNo("Is this matrix correct (y\\n)?")
    return matrix

#converts matrix to string form
def matrixToString(matrix):
    #search for greatest length element
    maxlen =  0
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            if len(str(matrix[i][j])) > maxlen:
                maxlen = len(str(matrix[i][j]))
    #print matrix
    maxlen += 2
    s = ""
    for i in range(0,len(matrix)):
        s += "|"
        for j in range(0,len(matrix[i])):
            s += " "*(maxlen-len(str(matrix[i][j]))) + str(matrix[i][j])
        s += "|\n"
    return s.rstrip()

def binaryMatrixPower(matrix, power):
    if (len(matrix)!=len(matrix[0])):
        print("Matrix not square!")
        return
    #solvedMatrices index represents matrix of power of 2 ** index
    count = 0
    solvedMatrices = [matrix]
    i = 1
    c = 0
    while i * 2 <= power:
        i *= 2
        c += 1
        solvedMatrices.insert(c,matrixMult(solvedMatrices[c-1],solvedMatrices[c-1]))
        count+=1
    #start with biggest matrix
    result = solvedMatrices[len(solvedMatrices)-1]
    power -= i
    while power > 0:
        if i <= power:
            result = matrixMult(result, solvedMatrices[c])
            count+=1
            power -= i
        i /= 2
        c -= 1
    print("Number of multiplications performed: "+str(count))
    return result

#raises a given matrix to a given power
def matrixPower(matrix, power):
    result = []
    resultSet = False
    while power > 0:
        if power & 1 == 1:
            if resultSet: result = matrixMult(result, matrix)
            else:
                result = matrix
                resultSet = True
        matrix = matrixMult(matrix, matrix)
        power >>= 1
    return result

#rounds all elements of matrix to the given number of decimals
def roundMatrix(matrix, numDecimals):
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            matrix[i][j] = round(matrix[i][j],numDecimals)
    return matrix

#inputs with type checking and message on type failure
def safeInput(message, failMessage, type2Check):
    while True:
        var = input(message+"\n")
        if var == "quit": quit()
        try: var = type2Check(var)
        except ValueError: print(failMessage, end=" ")
        else: break
    return var

#prompt to save var
def promptSave(var):
    while promptYesNo("Do you want to save new object to a file (y\\n)?"):
        fileName = safeInput("What do you want the file name to be?","Invalid file name.",str)+".txt"
        if os.path.isfile(fileName):
            if promptYesNo("File already exists. Overwrite (y\\n)?"):
                f = open(fileName, "w")
                f.write(var)
                f.close()
                print("File saved as '"+fileName+".'")
                break
        else:
            f = open(fileName,"w")
            f.write(var)
            f.close()
            print("File saved as '"+fileName+".'")
            break
    else:
        print("File not saved.")

#prompt to load matrix from file
def matrixFromFile():
    done = False
    while not done:
        fileName = safeInput("What is the name of the file?","Invalid file name.",str)+".txt"
        if os.path.isfile(fileName):
            f = open(fileName, "r")
            string = f.read()
            f.close()
            string = string.replace("|","").split("\n")
            for i in range(0,len(string)):
                string[i] = string[i].split()
            for i in range(0,len(string)):
                for j in range(0,len(string[i])):
                    string[i][j] = float(string[i][j])
            print(matrixToString(string))
            done = promptYesNo("Is this matrix correct (y\\n)?")
        else:
            print("Invalid file name. ", end="")
    return string

#prompt yes or no question
def promptYesNo(message):
    while True:
        prompt = input(message+"\n")
        if prompt == "quit": quit()
        if prompt == "y":return True
        if prompt == "n": return False
        else: print("Input must either be 'y' for yes or 'n' for no.", end="")

#prompt for new matrix
def promptNewMatrix():
    if promptYesNo("Do you want to load matrix from a file (y\\n)?"): return matrixFromFile()
    else: 
        matrix = newMatrix()
        promptSave(matrixToString(matrix))
        return matrix


print("------------------------------------------------------\n"
    + "Type 'quit' at any time to exit the program.\n"
    + "------------------------------------------------------")
#initial prompting for matrix
matrix = promptNewMatrix()
while True:
    fail = False
    while True:
        operation = safeInput("What operation would you like to perform? Type '1' for multiplication or '2' for exponents.", "Input must be an integer.",int)
        if operation == 1:
            print("One more matrix is needed. Remember that order matters. ",end="")
            matrix2 = promptNewMatrix()
            result = matrixMult(matrix, matrix2)
            if result == None: fail = True
            break
        if operation == 2:
            initialTime = time.time()
            result = matrixPower(matrix,safeInput("Raise matrix to what power?","Input must be an integer.",int))
            totalTime = time.time() - initialTime
            print(f"Total time taken: {totalTime:0.3f} milliseconds.")
            break
        else: print("Invalid input.", end="")
    if not fail:
        result = roundMatrix(result, safeInput("Round to how many decimal places?","Input must be an integer.",int))
        print(matrixToString(result))
        promptSave(matrixToString(result))
    else:
        print("Operation failed. ", end="")
    #prompt continue and reuse
    if not promptYesNo("Want to calculate more (y\\n)?"): break
    if not promptYesNo("Do you want to keep using the current matrix (y\\n)?"): matrix = promptNewMatrix()

print("Program terminated.")