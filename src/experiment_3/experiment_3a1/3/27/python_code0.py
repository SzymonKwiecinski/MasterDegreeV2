import pulp
import json

# Load data from the given JSON
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

# Extract data from the dictionary
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of possible cities

# Create a linear programming problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
problem += pulp.lpSum(communication[k][j] * cost[l][m] * islocated[k][l] 
                      for k in range(K) for l in range(L) for j in range(K) for m in range(len(cost[0]))) \
                      - pulp.lpSum(benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)), "Total_Cost"

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1, f"Dept_{k}_Location"

# No more than three departments may be located in any city
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3, f"Max_Dept_in_City_{l}"

# Solve the problem
problem.solve()

# Output the decision variable matrix
for k in range(K):
    for l in range(L):
        print(f'Department {k+1} is located in city {l+1}: {pulp.value(islocated[k][l])}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')