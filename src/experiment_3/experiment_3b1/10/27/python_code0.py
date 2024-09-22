import pulp
import json

# Data provided in JSON format
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

# Extracting data from JSON
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Define the problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective Function
objective_terms = []
for k in range(K):
    for l in range(L):
        communication_cost = sum(communication[k][j] * cost[l][m] * islocated[k][l] for j in range(K) for m in range(L))
        objective_terms.append(communication_cost)
        objective_terms.append(-benefit[k][l] * islocated[k][l])

problem += pulp.lpSum(objective_terms), "Total Cost"

# Constraints
# Each department can only be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1, f"One_City_for_Department_{k}"

# No city can accommodate more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3, f"Max_Departments_in_City_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')