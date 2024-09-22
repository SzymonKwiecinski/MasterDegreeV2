import pulp
import json

# Data in JSON format
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
L = range(len(data['communication'][0]))  # Cities

# Initialize problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), cat='Binary')

# Objective Function
objective = pulp.lpSum(
    data['communication'][k][j] * data['cost'][j][l] * (1 - islocated[k][l]) 
    for k in K for l in L for j in K
) - pulp.lpSum(
    data['benefit'][k][l] * islocated[k][l] 
    for k in K for l in L
)

problem += objective

# Constraints

# Location Limitations
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) <= 1, f"Location_Limit_k_{k}"

# City Capacity
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3, f"City_Capacity_l_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')