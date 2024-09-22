import pulp
import json

# Data from the provided JSON
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                      [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                      [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Define sets
K = range(len(data['benefit']))  # Departments
L = range(len(data['benefit'][0]))  # Cities

# Define the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(data['communication'][k][j] * data['cost'][l][m] * islocated[k][l] 
                for k in K for l in L for j in K for m in range(len(data['cost'][0])))
    - pulp.lpSum(data['benefit'][k][l] * islocated[k][l] for k in K for l in L)
)

# Constraints
# Each department can only be located in one city
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) == 1

# No city can have more than three departments
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3

# Solve the problem
problem.solve()

# Output the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')