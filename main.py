# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN
# Author: Freddie Seidler
# CID: 01385931
# ####################################################



# Method:
# 1. Take the input matrix and change the values of any target point to a new metric (the number of other target points around that point).
# 2. For each shape, check if it can be placed at the point being considered,
#    if it can, return a metric (based upon the sum of each point that shape is covering).
# 3. Place the shape with the lowest metric in a separate solution matrix.
# 4. Update the input matrix to indicate that another shape cannot be placed in the points covered by the newly placed shaped.
# 5. Once the code has iterated through every point, the code goes back through every point seeing if a shape
#    can be placed in an area filling up 3 missing blocks and 1 excess block, increasing the accuracy. 
# 6. The solution is returned.


# Use of paradigms of algorithm design:
# 1. The general approach used in this solution is greedy, shapes are placed with little consideration for future shapes.
# 2. There is some optimality used in my approach. A metric is used to help determine which shape to place.
# 3. There is an element of recursiveness in the solution, however there is not a fully recursive function.
#    The 'Tetris' function calls a function very similar to itself to increase the accuracy.




# The shapes available to be placed (forbidden shapes are not included in this list).
# They are referenced on the global scale because all the functions require the list. 
shapes = [[[0, 0], [1, 0], [2, 0], [2, 1]], [[0, 0], [1, -2], [1, -1], [1, 0]], [[0, 0], [0, 1], [1, 1], [2, 1]], [[0, 0], [0, 1], [0, 2], [1, 0]],[[0, 0], [1, 0], [2, -1], [2, 0]], [[0, 0], [0, 1], [0, 2], [1, 2]], [[0, 0], [0, 1], [1, 0], [2, 0]], [[0, 0], [1, 0], [1, 1], [1, 2]], [[0, 0], [1, 0], [1, 1], [2, 0]], [[0, 0], [1, -1], [1, 0], [1, 1]], [[0, 0], [1, -1], [1, 0], [2, 0]], [[0, 0], [0, 1], [0, 2], [1, 1]], [[0, 0], [0, 1], [1, -1], [1, 0]], [[0, 0], [1, 0], [1, 1], [2, 1]], [[0, 0], [0, 1], [1, 1], [1, 2]],[[0, 0], [1, -1], [1, 0], [2, -1]]]


def neighbours(matrix):
    
    """This function takes the given matrix (this has been edited from the original matrix, see below),
    and cycles through each point.
    It changes the value of each point to a 1, 2, 3 or 4, depending on how many points surrounding it
    are target points. N.B It only searches up, down, left and right - not diagonally."""
    
    rows = len(matrix)
    columns = len(matrix[1])
    for row in range(rows):
        for column in range(columns):                               # Cycling through each point in the matrix
            num_neighbours = 0                                      # This initiates the variable that will become the new value for that point within the matrix
            if matrix[row][column] == 1:                            # This loop checks in turn the point left, right, above and below the selected point for a neighbour
                if column - 1 >= 0 and matrix[row][column - 1] != 0 and matrix[row][column - 1] != 88:          # The point being checked !=0 or 88 as these points are either not within
                    num_neighbours += 1                                                                         # the target area, or are out of bounds.
                if column + 1 <= columns and matrix[row][column + 1] != 0 and matrix[row][column + 1] != 88:    # The number 88 was choosen to indicate invalid points as it is clearly identifiable during print statement error checking.
                     num_neighbours += 1                                                                        # I also had to ensure that I did not accientally check a point at the end of
                if row - 1 >= 0 and matrix[row - 1][column] != 0 and matrix[row - 1][column] != 88:             # a row, or the last row, by accident (e.g if I looked at matrix[0][-1]).
                    num_neighbours += 1
                if row + 1 <= rows and matrix[row + 1][column] != 0 and matrix[row + 1][column] != 88:
                    num_neighbours += 1                                 
                matrix[row][column] = num_neighbours                # The matrix is then updated with its new values.     
    return matrix


def shapeSelector(matrix, i, j):
    
    ''' This function determines if a shape can be placed from selected point.
     It returns the index of the best shape (as determined by my method) from the list 'shapes'
     It will take a metric, produced for each shape, and store the lowest value.
     N.B I could have stored the metrics and shapeIDs of all shapes that could be placed in a dictionary,
     and then run a QuickSort algorithm to return the shapeID with the lowest metric.
     I decided against this as it would have added unecessary lines of code, reducing the conciseness and elegance of my code.'''
    
    
    bestCurrentValue = 100                                              # This is the variable that stores the metric, it is initiated at 100, as the max value it could ever be is 16 (4x4)
    bestShapeID = 100                                                   # This is the variable that stores the index of the best shape, it is initiated at 100 as the index returned could be 0-15
    for shape in shapes: 
        sumNeighbourValues = neighboursChecker(i, j, shape, matrix)     # This function is explained below. 
        if sumNeighbourValues == 0:                                     # If the value returned is 0, a shape cannot be placed, and so the bestCurrentValue is not updated.
            pass                                                        # The function then checks if next shape can be placed.
             
        elif (sumNeighbourValues !=0 and sumNeighbourValues < bestCurrentValue):   
            bestCurrentValue = sumNeighbourValues
            bestShapeID = shapes.index(shape)                           # Updating the variable with index of the best shape, to be used to give the shapeID that will be placed.
    return bestShapeID


def neighboursChecker(i, j, shape, matrix):
    
    ''' This function will sum the values of each point the shape that is being considered covers.
     If the value = 0 (a non-target-area point) or 88 (an out-of-bounds point) a value of 0 is returned.'''
    
    
    sumNeighbourValues = 0
    for m in range(4):                                     # range(4) as there will always be 4 co-ordinates to check for each shape.
        k = i + shape[m][0]
        l = j + shape[m][1]
        
        neighbourValue = matrix[k][l]                      # Initating the variable for the value of each point.
        if (neighbourValue == 0 or neighbourValue == 88):  # A disqualifying statement - the selected shape cannot fit, so move on. 
            sumNeighbourValues = 0
            return sumNeighbourValues
        
        else:
            sumNeighbourValues += neighbourValue
    return sumNeighbourValues
        
        
def matrixEditor(matrix, i, j, bestShapeID):
    
    ''' This function edits the matrix I am working on.
     It replaces any point where a shape has been placed with the value 88.
     (This was choosen as it is a very identifiable number for error checking with print statements.)
     This will ensure that any point where a shape has been placed cannont be considered again, or have another shape placed over it.'''
    
    shape = shapes[bestShapeID]
    for a in range(4):
        b = i + shape[a][0]
        c = j + shape[a][1]
        matrix[b][c] = 88
    return matrix


def shapePlacer(solutionMatrix, bestShapeID, i, j, shapeCount):
    
    ''' This function places the infomation required by the brief (tuples of shapeID and a shape count) into my solution matrix.
     It runs in a very similar way to the previous functions, by traversing through each point in for loops.'''
    
    
    shape = shapes[bestShapeID]
    for a in range(4):
        b = i + shape[a][0]
        c = j + shape[a][1]
        solutionMatrix[b][c] = (bestShapeID + 4,shapeCount)    # My list of shapes does not include the forbidden shapes, so to ensure my solution is 
    return solutionMatrix                                      # valid, I have to +4 to my ID variable.


def finalSolution(solutionMatrix):
    
    ''' This function trims the matrix I am working on back to its original size.
     The inbuilt .pop() removes the specified term from the list.
     I want to remove the pad of 88s I added at the start of my Tetris function.'''
    
    solutionMatrix.pop(-1)                                     # These lines remove the first and last two rows.
    solutionMatrix.pop(-1)
    solutionMatrix.pop(0)
    solutionMatrix.pop(0)
    M = []
    for row in solutionMatrix:                                 # These lines remove the first and last two columns (by slicing each row).
        new_row = row[2:-2]
        M.append(new_row)
    return M

def push(matrix, mRows, mCols, shapeCount,solutionMatrix):
    
    ''' The following functions (any defined as pushXXXXX) are designed to increase the accuracy of my final solution.
     It is essentially running my entire code again, however this time shapes can be placed over non-target areas.
     By placing shapes where there are 3 target points, next to a non-target point, I am reducing my number of missing
     blocks by 3, and only increasing my excess blocks by 1.'''
    
    for i in range(mRows):
        for j in range(mCols):
            if matrix[i][j] != 0 and matrix[i][j]!= 88:                                # The same rules as previous apply, so no shape can be placed
                bestPushShapeID = pushShapeSelector(matrix, i, j)                      # over another shape, or out of bounds.
                if bestPushShapeID == 100:
                    pass
                
                else:                                                                  # All the variables have been renamed with 'push' included to clearly identify them.
                    shapeCount +=1                                                     # Apart from the shapeCount, this has to be inherited from the main Tetris function.
                    
                    pushMatrixEditor(matrix, i, j, bestPushShapeID)
                    pushShapePlacer(solutionMatrix, bestPushShapeID, i, j, shapeCount)
            else:
                pass
            
    return solutionMatrix
                

def pushShapeSelector(matrix, i, j):
    
    ''' This function runs the same as 'shapeSelector'.'''
    
    bestCurrentValue = 100
    bestPushShapeID = 100
    for shape in shapes: 
        sumNeighbourValues = pushNeighboursChecker(i, j, shape, matrix)
        if sumNeighbourValues == 0:
            pass
             
        elif (sumNeighbourValues !=0 and sumNeighbourValues < bestCurrentValue):   
            bestCurrentValue = sumNeighbourValues
            bestPushShapeID = shapes.index(shape)     
    return bestPushShapeID


def pushNeighboursChecker(i, j, shape, matrix):
    
    ''' This function runs the same as 'neighboursChecker' with a slight addition.
     A count was added, so that for every neighbourValue != 0 or 88, the count increased by 1.
     A shape cannot be placed if this count is < 3.
     This prevents my 'push' functions placing a shape in an area of 1 target point, with 3 non-target points etc.'''
    
    sumNeighbourValues = 0
    count = 0
    for m in range(4):
        k = i + shape[m][0]
        l = j + shape[m][1]
        
        neighbourValue = matrix[k][l]
        if (neighbourValue == 88):
            sumNeighbourValues = 0
            return sumNeighbourValues
        
        elif neighbourValue != 0:
            sumNeighbourValues += neighbourValue
            count+=1
            
    if count < 3:                                  # The qualifying statement to ensure that any shape placed will improve the accuracy.
        sumNeighbourValues = 0
    return sumNeighbourValues


def pushMatrixEditor(matrix, i, j, bestPushShapeID):
    
    ''' This function runs the same as 'matrixEditor'.'''
    shape = shapes[bestPushShapeID]
    for a in range(4):
        b = i + shape[a][0]
        c = j + shape[a][1]
        matrix[b][c] = 88
    return matrix



def pushShapePlacer(solutionMatrix, bestPushShapeID, i, j, shapeCount):

    ''' This function runs the same as 'shapePlacer'.''' 
    shape = shapes[bestPushShapeID]
    for a in range(4):
        b = i + shape[a][0]
        c = j + shape[a][1]
        solutionMatrix[b][c] = (bestPushShapeID + 4,shapeCount)
    return solutionMatrix


def Tetris(target):
    
    ''' This is my main function, that finds a solution by calling all the pre-defined functions.
     It will run through the core functions once, before calling the 'push' function to increase the accuracy of the final solution.
     This 'push' function is acting in an almost recursive nature, it has the same code as the 'Tetris' function,
     but has the variables named differently to allow for shapes being placed over non-target points.'''
    
    print("Initiating Solution")                                   # This is an error checking print statement. Occasionally my laptop was unable to generate the target,
                                                                   # this was a way of seeing if my code had been called or not by 'performance_std'.
    width = len(target[0])
    height = len(target)
    matrix = [[88 for _ in range(width+4)] for __ in range(2)]     # These lines edit the input matrix, by padding it with the value 88, with two rings around the matrix. 
    for row in target:                                             # This pad was done, so that I do not accidentally cause errors by attempting to place shapes out side of the
        matrix.append([88] + [88] + row + [88] + [88])             # of the target matrix.
    matrix.append([88 for _ in range(width+4)])
    matrix.append([88 for _ in range(width+4)])
    N = len(matrix) 
    M = len(matrix[0])
    solutionMatrix = [[(0,0)] * M for i in range(N)]               # Generating the matrix for my solutions to be placed into. This will be the size of the padded matrix, 
    mRows = len(matrix)                                            # but this is then trimmed back in the 'finalSolution' function. 
    mCols = len(matrix[0])

    neighbours(matrix)                                             # I begin by calling this function to update my matrix with the values of the 
                                                                   # metric that I use to select which shape to place. 
    shapeCount = 0
    for i in range(mRows):
        for j in range(mCols):
            if matrix[i][j] != 0 and matrix[i][j]!=88:             # Initially, I do not try to place a shape on a non-target point or one that is out of bounds/has a shape already placed.
                bestShapeID = shapeSelector(matrix, i, j)          # Calling this function to determine which shape is best to place in this location.
                if bestShapeID == 100:                             # 'shapeSelector' will return a value of 100 if no shape can be placed, so the function does nothing else and moves to the next point.
                    pass
                
                else:
                    shapeCount +=1                                 # A shape can be successfully placed, so the functions that begin to generate a solution are called.
                                                                   # The shape count is then updated each time it is determined a shape can be placed. 
                    matrixEditor(matrix, i, j, bestShapeID)
                    shapePlacer(solutionMatrix, bestShapeID, i, j, shapeCount)
                
            else:                                                  # This pass statement moves the location to the next point. The point currently being considered cannont have a shape placed over it. 
                pass
            
    a = push(matrix, mRows, mCols, shapeCount, solutionMatrix)     # Once 'Tetris' has produced an OK solution, 'push' is called to improve the final solution's accuracy.

    M = finalSolution(a)                                           # The final step before returning a solution is to trim off the pad that was added initially. 
    
    return M
    
