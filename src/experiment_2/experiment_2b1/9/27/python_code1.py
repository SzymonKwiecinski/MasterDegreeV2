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

# Problem setup
K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Create a LP problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Create decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function: minimize the overall yearly cost
total_cost = pulp.lpSum(
    -data['benefit'][k][l] * islocated[k][l] 
    for k in range(K) for l in range(L)
)

# Adding communication costs to the objective function
for k in range(K):
    for l in range(L):
        communication_cost = pulp.lpSum(
            data['communication'][k][j] * data['cost'][l][m] * islocated[j][m]
            for j in range(K) for m in range(L)
        )
        total_cost += communication_cost * islocated[k][l]

problem += total_cost

# Constraints
# Each department must either be located in a city or remain in London (represented by 0)
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) <= 3  # At most 3 departments per city

# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# Solve the problem
problem.solve()

# Prepare output
islocated_output = [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]

# Print the output
output = {
    "islocated": islocated_output
}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')