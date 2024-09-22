import pulp
import json

# Input data
data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                         [0.0, 0.0, 1.4, 1.2, 0.0], 
                         [1.0, 1.4, 0.0, 0.0, 2.0], 
                         [1.5, 1.2, 0.0, 2.0, 0.7], 
                         [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], 
                 [15, 5, 9], 
                 [13, 9, 10]]}

# Extracting data
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities (including London)

# Create the problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
total_cost = pulp.lpSum(
    - benefit[k][l] * islocated[k][l] + 
    pulp.lpSum(communication[k][j] * cost[l][m] * islocated[j][m] for j in range(K) for m in range(L)) * islocated[k][l] 
    for k in range(K) for l in range(L)
)

problem += total_cost

# Constraints
# Each department should be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No more than 3 departments can be located in the same city
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare output
islocated_output = [[int(islocated[k][l].value()) for l in range(L)] for k in range(K)]

output = {"islocated": islocated_output}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')