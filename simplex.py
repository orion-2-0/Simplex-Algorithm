# import numpy as np

def print_matrix(matrix):
    for row in matrix:
        print("  ".join(map(str, row)))
    print(' \n')


def sumColumn(A,col_index):
    sum = 0
    for i in range(len(A)):
        sum += A[i][col_index]
    return sum



def performOperations(T,pivotRow, pivotCol):

    pivotElement = T[pivotRow][pivotCol]

    for i in range(1,len(T)):
        if(i==pivotRow):
            continue

        u=(T[i][pivotCol]/pivotElement)
        for j in range(1,len(T[0])):
            T[i][j]-=u*T[pivotRow][j]


    for j in range(1,len(T[0])):
        T[pivotRow][j] = ((T[pivotRow][j])/(pivotElement))


    T[pivotRow][0] = T[0][pivotCol]
    return T



def read_input(filename):
    
    with open(filename, 'r') as f:
        lines = f.readlines()

    objective = None # 1  -> minimize # -1 -> maximize
    A = []
    b = []
    c = []
    constraint_types = []
    neg_row = []
    cons_row = []
     
    num_constraints = 0
    decision_vars = 0
    slack_vars = 0

    myDict = {}

    mode = "objective"

    for line in lines:
        line = line.strip()
        
        if not line :
            continue
        
        if line == "[objective]" :
            mode = "objective"
            continue
        


        elif (line == "[A]"):
            mode = "A"
            continue
        
        elif line == "[b]":
            mode = "b"
            continue

        elif line == '[c]':
            mode = 'c'
            continue

        elif line == '[constraint_types]':
            mode = 'constraint_types'
            continue
        
        
        elif mode == "objective":
            if(line.lower() == "maximize"):
                objective = -1
            else:
                objective = 1


        elif mode == "A":
            row_entries = line.split(',')
            decision_vars = len(row_entries)
            row_entries = [int(x) for x in row_entries]
            A.append(row_entries)
        
        elif mode == "b":

            b.append(int(line))
            if (int(line) < 0):
                neg_row.append(1)
            else:
                neg_row.append(0)
            
        
        elif mode == "c":
            row_entries = line.split(',')
            c = [int(x) for x in row_entries]
           

        elif mode == "constraint_types":

            if (line == ">="):
                cons_row.append(-1)

            elif (line == "="):
                cons_row.append(0)
            else:
                cons_row.append(1)


    num_constraints = len(neg_row)

    for i in range(len(neg_row)):
        if neg_row[i]:
            A[i] = [-x for x in A[i]]
            b[i] = - b[i]
            cons_row[i] = -cons_row[i]
    
    c = [x*objective for x in c]


    for i in range(num_constraints):
        if (cons_row[i] != 0):

            slack_vars += 1
            for j in range (num_constraints):
                if j == i:
                    A[j].append(cons_row[i])
                else:
                    A[j].append(0)
    

    for i in range(decision_vars):
        myDict[i] = "decision_vars"
    
    for i in range(decision_vars,decision_vars + slack_vars):
        myDict[i] = "slack_vars"
    
    # A = np.array(A)
    # b = np.array(b)
    # c = np.array(c)
    

    # print("decision_vars : ",  decision_vars, "slack_vars : ", slack_vars, "\n")
        
    # print(f"A : {A} \n b : {b} \n c : {c} \n cons_row : {cons_row} \n neg_row : {neg_row} \n myDict {myDict}")
        
    return A,b,c,myDict

def phase_I (A, b, myDict):
    
    num_vars = len(A[0])
    num_constraint = len(b)
    aux_vars = num_constraint

    c = [0 for i in range(num_vars)]
    for i in range(aux_vars):
        c.append(1)
    
    for i in range(num_vars, aux_vars + num_vars):
        myDict[i] = "auxillary_vars"

    

    for i in range(num_constraint):
        for j in range(num_constraint):
            if (i == j):
                A[j].append(1)
            else:
                A[j].append(0)

    
    print(f"A:{A} \n c : {c} \n myDict : {myDict}")
    
    row1 = [0, 0]
    for i in range(aux_vars + num_vars):
        row1.append(i)
    
    
    ctx = 0
    for value in b:
        ctx += value

    row2 = [0,-ctx]
    
    for i in range(num_vars):
        row2.append(-sumColumn(A,i))

    for i in range(num_vars, num_vars + aux_vars):
        row2.append(0)
    

    T = [[(f'x_{i}_{j}') for i in range(aux_vars + num_vars + 2)] for j in range(num_constraint + 2)]
    T[0] = row1
    T[1] = row2

    for i in range(2,num_constraint + 2):
        T[i][0] = num_vars + i - 2
        T[i][1] = b[i-2]
            

    for j in range(2, num_vars + aux_vars + 2):
        for i in range(2, num_constraint+2):
            T[i][j] = A[i-2][j-2]

       
    print("initial matrix \n")
    print_matrix(T)
    print('\n')

    # pl = [[5,5],[5,4],[3,3],[2,2]]
    # for item in pl:
    #     print(f"pivot element : {T[item[0]][item[1]]}")
    #     T = performOperations(T,item[0],item[1])
    #     print_matrix(T)

    
    done = 0

    status = 0 #0 for feasible,1 for infeasible , 2 for unbdd.
    while (done == 0):
        
        done = 1
        pivotRow = -1
        pivotCol = -1
        for col in range(2,num_vars+aux_vars+2):

            if(T[1][col] < 0):
                pivotCol = col
            
            if(pivotCol == -1):
                continue

            lastIndex = -1
            min_value = 1000000 #some large value
            
            for i in range (2 , num_constraint + 2):
                if (T[i][pivotCol] > 0):
                    print (f"{T[i][pivotCol]}")
                    print (f"{T[i][1]}")
                    temp = T[i][1] / T[i][pivotCol]
                    print ("temp : ", temp)
                    if (temp < min_value):
                        lastIndex = i
                        min_value = temp
            
            print ("lastindex : ", lastIndex)
            
            print ("--------------")
            if (min_value == 1000000):
                status = 1
                break

            pivotRow = lastIndex
        
        if status == 0 :
            print("T[1]:")
            print(T[1])
            # check if cost of solution < 0 or =0
            # if cost < 0 , infeasible
            #if cost = 0, driving variable out of basis
            break
        
        if status == 1 :
            print("T[1]:")
            print(T[1])
            break
        
        done = 0
        # transformation and run the while loop again
        print(pivotRow , pivotCol, "\n")
        T = performOperations(T,pivotRow,pivotCol)
        

        
    
    if status == 0 :
        if -T[1][1] > 0 : 
            status = 1
        elif T[1][1] == 0:
            #drive variable out of basis
            pass        
                
    if (status == 1):
        print ("infeasible !!!!!")
           
    print_matrix(T)
    
    return A,c

A,b,c,myDict = read_input("input2.txt")
phase_I(A,b,myDict)
