import pulp
import json

data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], 'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}

K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities (including London)

# Initialize the problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function: Minimize the total costs
total_cost = pulp.lpSum(
    data['communication'][k][j] * data['cost'][l][m] * islocated[k][l]
    for k in range(K)
    for l in range(L)
    for j in range(K)
    for m in range(L)
)

total_benefit = pulp.lpSum(
    data['benefit'][k][l] * islocated[k][l]
    for k in range(K)
    for l in range(L)
)

problem += total_cost - total_benefit

# Constraints: Limit the number of departments in each city to 3
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3, f"Max_departments_in_city_{l}"

# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1, f"One_location_for_department_{k}"

# Solve the problem
problem.solve()

# Output the results
islocated_output = [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]

output = {
    "islocated": islocated_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')