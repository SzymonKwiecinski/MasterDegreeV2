import pulp
import json

# Data
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # number of departments
L = len(cost[0])  # number of cities

# Initialize the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective Function
problem += pulp.lpSum(-benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)) + \
           pulp.lpSum(communication[k][j] * cost[m][l] * islocated[k][l] * islocated[j][m] 
                       for k in range(K) for j in range(K) for l in range(L) for m in range(L))

# Constraints
# Each department is located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city hosts more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')