Python Code for solving Linear Programming Problems (LPPs).

Learn more about Simplex Algorithm [here](https://www.jeremykun.com/2014/12/01/linear-programming-and-the-simplex-algorithm/)

Make a file input.txt in the same directory.
Your A, b, and c matrices, along with the constraint types and objective (‘maximize’ or ‘minimize’), 
should be taken as input from a text file (input.txt) following the specified format. An example of the  
same has been provided.  
1. The [objective] section should clearly state whether the problem is a "maximize" or 
"minimize" problem. This will dictate the direction of your optimization in solving the problem.  
2. The [A] section contains the coefficients of the variables in the linear constraints. Each row in 
this section represents a constraint, and each column corresponds to a variable.  
3. The [b] section lists the right-hand side (RHS) values for each constraint, with each row 
corresponding to a constraint in the [A] section.  
4. The [constraint_types] section specifies the type of each constraint corresponding to the rows 
in [A] and [b]. Use <= for less than or equal to, >= for greater than or equal to, and = for equality 
constraints.  
5.  The [c] section contains the coefficients of the objective function's variables in one row.

Sample Input :  
```
[objective]
maximize

[A]  
1, 2, 3  
4, 5, 6  
7, 8, 9  
  
[b]  
10  
11  
12  
  
[constraint_types]

<=  
>=  
=

  
[c]  
2, 4, 6
```  

Output will be like :  
- Initial Tableau (initial_tableau)  
- Final Tableau (final_tableau)  
- Status of Solution (solution_status) : “optimal”/ “infeasible”/ “unbounded”  
- Optimal Solution Vector (optimal_solution): It will return the optimal solution 
vector x*, which contains the values of the decision variables [x1, x2, ..., xn] that maximize or 
minimize the objective function, depending on the problem statement. This vector will be 
in a standardized format, such as a NumPy array.  
- Optimal Value (optimal_value): Real values
The format of the tableau will be like a matrix having m rows, where m is the number of equations 
given in constraints and the columns will be as follows: first column for the values of current BFS, 
followed by the variables in optimization problem, followed by slack/surplus variables, and finally 
artificial variables
