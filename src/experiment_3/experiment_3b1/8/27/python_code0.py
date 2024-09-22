import pulp
import json

# Given data in JSON format
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                      [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                      [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Extracting sets and parameters
K = range(len(data['benefit']))  # Departments
L = range(len(data['cost']))      # Cities

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), cat='Binary')

# Objective Function
objective = pulp.lpSum(
    communication[k][j] * cost[l][j] * islocated[k][l] 
    for k in K for l in L for j in K
) - pulp.lpSum(
    benefit[k][l] * islocated[k][l] 
    for k in K for l in L
)

problem += objective

# Constraints
# Each department can be located in only one city
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) == 1, f"One_City_{k}"

# No city can host more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3, f"Max_Departments_{l}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')