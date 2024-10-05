import pulp

# Load data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [
        [0.0, 0.0, 1.0, 1.5, 0.0], 
        [0.0, 0.0, 1.4, 1.2, 0.0], 
        [1.0, 1.4, 0.0, 0.0, 2.0], 
        [1.5, 1.2, 0.0, 2.0, 0.7], 
        [0.0, 0.0, 2.0, 0.7, 0.0]
    ],
    'cost': [
        [5, 14, 13], 
        [15, 5, 9], 
        [13, 9, 10]
    ]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

num_departments = len(benefit)
num_cities = len(benefit[0])

# Define problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", 
                                  [(k, l) for k in range(num_departments) for l in range(num_cities)],
                                  cat='Binary')

# Objective function
total_benefit = pulp.lpSum(islocated[k, l] * benefit[k][l] 
                           for k in range(num_departments) for l in range(num_cities))
total_communication_cost = pulp.lpSum(islocated[k, l] * islocated[j, m] * communication[k][j] * cost[l][m]
                                      for k in range(num_departments) 
                                      for j in range(num_departments)
                                      for l in range(num_cities)
                                      for m in range(num_cities))

problem += total_communication_cost - total_benefit

# Constraints

# Each department must be located in exactly one city
for k in range(num_departments):
    problem += pulp.lpSum(islocated[k, l] for l in range(num_cities)) == 1

# No more than three departments can be located in the same city
for l in range(num_cities):
    problem += pulp.lpSum(islocated[k, l] for k in range(num_departments)) <= 3

# Solve problem
problem.solve()

# Prepare output
output = {
    "islocated": [
        [pulp.value(islocated[k, l]) for l in range(num_cities)]
        for k in range(num_departments)
    ]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')