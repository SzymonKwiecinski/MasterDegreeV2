import pulp
import json

# Input data in JSON format
data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                         [0.0, 0.0, 1.4, 1.2, 0.0], 
                         [1.0, 1.4, 0.0, 0.0, 2.0], 
                         [1.5, 1.2, 0.0, 2.0, 0.7], 
                         [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], 
                 [15, 5, 9], 
                 [13, 9, 10]]}

# Extract data
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities

# Create the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variable: islocated[k][l] == 1 if department k is located in city l
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function: Minimize the total cost
total_cost = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
    for k in range(K)
    for j in range(K)
    for l in range(L)
    for m in range(L)
)
total_benefit = pulp.lpSum(
    benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)
)

# The objective is to minimize total cost minus total benefit
problem += total_cost - total_benefit

# Constraints: Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# Constraints: No city can have more than 3 departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare output
islocated_result = [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the results
output = {"islocated": islocated_result}
print(json.dumps(output))