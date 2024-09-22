import pulp
import numpy as np
import json

# Input data in JSON format
data = '''
{
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                     [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                     [0.0, 0.0, 2.0, 0.7, 0.0]], 
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}
'''

# Load data
data = json.loads(data)

benefit = np.array(data['benefit'])
communication = np.array(data['communication'])
cost = np.array(data['cost'])

num_departments = len(benefit)
num_cities = len(cost)

# Create the LP problem
problem = pulp.LpProblem("Department_Relocation_Problem", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", 
                                    ((k, l) for k in range(num_departments) for l in range(num_cities)), 
                                    cat='Binary')

# Objective Function
problem += pulp.lpSum(
    communication[k, j] * cost[l, m] * islocated[(k, l)] 
    for k in range(num_departments)
    for l in range(num_cities)
    for j in range(num_departments)
    for m in range(num_cities)
) - pulp.lpSum(
    benefit[k, l] * islocated[(k, l)] 
    for k in range(num_departments)
    for l in range(num_cities)
)

# Constraints
# Each department must be located in exactly one city
for k in range(num_departments):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(num_cities)) == 1

# No city can host more than three departments
for l in range(num_cities):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(num_departments)) <= 3

# Solve the problem
problem.solve()

# Output the result
islocated_result = [[int(islocated[(k, l)].value()) for l in range(num_cities)] for k in range(num_departments)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')