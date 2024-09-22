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

# Define the problem
K = len(data['benefit'])  # number of departments
L = len(data['benefit'][0])  # number of cities

problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
communication_cost = pulp.lpSum(
    data['communication'][k][j] * data['cost'][l][m] * islocated[k][l]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)
benefit = pulp.lpSum(
    data['benefit'][k][l] * islocated[k][l] for k in range(K) for l in range(L)
)
problem += communication_cost - benefit, "Total_Cost"

# Constraints
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) <= 1, f"One_location_for_department_{k}"

for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3, f"Max_three_departments_in_city_{l}"

# Solve the problem
problem.solve()

# Prepare output
islocated_result = [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {"islocated": islocated_result}
print(output)