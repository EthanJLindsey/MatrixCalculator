#inputs two nested lists where each element in each matrix is one row
def matrixMult(matrix1, matrix2):
    #x and y iterate through each place in the result
    if len(matrix1[0])!=len(matrix2):
        print("Incompatible matrices!")
        print("Matrix 1:")
        printMatrix(matrix1)
        print("Matrix 2:")
        printMatrix(matrix2)
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

def newMatrix():
    numRows = safeInput("How many rows does your matrix have?","The number of rows needs to be an integer.",int)
    numColumns = safeInput("How many columns does your matrix have?","The number of columns needs to be an integer.",int)
    matrix = []
    for i in range(0,numRows):
        matrix.append([])
        for j in range(0,numColumns):
            matrix[i].append(float(input("Row "+str(i+1)+" and Column "+str(j+1)+"? ")))
    return matrix

def printMatrix(matrix):
    #print matrix
    for i in range(0,len(matrix)):
        print("|",end="")
        for j in range(0,len(matrix[i])-1):
            print(str(matrix[i][j])+"   ", end="")
        print(str(matrix[i][len(matrix[i])-1]), end="")
        print("|")

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

def roundMatrix(matrix, numDecimals):
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            matrix[i][j] = round(matrix[i][j],numDecimals)
    return matrix

def safeInput(message, failMessage, type2Check):
    while True:
        try:
            var = input(message+"\n")
            if var == "exit":
                quit
            var = type2Check(var)
            break
        except ValueError:
            print(failMessage, end=" ")
    return var