import pulp
import json

# Data provided in JSON format
data = '''
{
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}
'''
datadict = json.loads(data)

# Parameters
benefit = datadict['benefit']
communication = datadict['communication']
cost = datadict['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities (including London)

# Create the problem variable
problem = pulp.LpProblem("Department_Location_Optimization", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
total_cost = pulp.lpSum(islocated[k, l] * (pulp.lpSum(communication[k][j] * pulp.lpSum(cost[l][m] * islocated[j, m] 
            for m in range(L)) for j in range(K)) - benefit[k][l]) for k in range(K) for l in range(L))
problem += total_cost

# Constraints
# Each department can be located in only one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than three departments can be located in the same city
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the output
islocated_matrix = [[int(islocated[k, l].varValue) for l in range(L)] for k in range(K)]
print("Location Matrix:")
for row in islocated_matrix:
    print(row)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')