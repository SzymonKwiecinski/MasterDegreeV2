import pulp
import json

# Data from the JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                     [0.0, 0.0, 1.4, 1.2, 0.0], 
                     [1.0, 1.4, 0.0, 0.0, 2.0], 
                     [1.5, 1.2, 0.0, 2.0, 0.7], 
                     [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], 
             [15, 5, 9], 
             [13, 9, 10]]
}

# Sets
K = range(len(data['benefit']))  # Departments
L = range(len(data['cost']))      # Cities

# Create the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), cat='Binary')

# Objective Function
problem += pulp.lpSum(islocated[k][l] * (pulp.lpSum(data['communication'][k][j] * 
                        pulp.lpSum(data['cost'][l][m] * islocated[j][m] for m in L) 
                        for j in K) - data['benefit'][k][l])
                        for k in K for l in L), "Total_Cost"

# Constraints
# Each department must be located in exactly one city
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) == 1, f"Dept_Assignment_{k}"

# No city may host more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3, f"City_Capacity_{l}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')