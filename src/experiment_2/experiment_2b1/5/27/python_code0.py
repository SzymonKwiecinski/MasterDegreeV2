import pulp
import json

# Input data from the prompt
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
K = len(benefit)  # number of departments
L = len(cost)     # number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), 0, 1, pulp.LpBinary)

# Objective function: Minimize costs considering benefits and communication costs
total_cost = pulp.lpSum([-benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)]) \
             + pulp.lpSum(communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m] 
                          for k in range(K) for j in range(K) for l in range(L) for m in range(L))
problem += total_cost

# Constraints
# Each department can be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# Each city can have at most 3 departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Output result
result = {"islocated": [[pulp.value(islocated[k][l]) for l in range(L)] for k in range(K)]}
print(json.dumps(result))

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')