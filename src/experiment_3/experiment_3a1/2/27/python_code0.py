import pulp
import json

# Data provided in JSON format
data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                         [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                         [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}

# Extracting number of departments and cities
K = len(data['benefit'])
L = len(data['benefit'][0])

# Create the LP problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", 
                                    ((k, l) for k in range(K) for l in range(L)), 
                                    cat='Binary')

# Objective function
problem += pulp.lpSum((-data['benefit'][k][l] * islocated[(k, l)] + 
                       pulp.lpSum(data['communication'][k][j] * data['cost'][l][j] * islocated[(k, l)] 
                                  for j in range(K)) 
                       for k in range(K) 
                       for l in range(L)), 
                       "Total_Cost")

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1, f"Location_Constraint_D_{k}"

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3, f"Max_Departments_City_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')