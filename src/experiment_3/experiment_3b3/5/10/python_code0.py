import pulp

# Data from JSON
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Define the optimization problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                          ((n, s, g) for n in range(data['N']) 
                                     for s in range(data['S']) 
                                     for g in range(data['G'])), 
                          lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[(n, s, g)] 
                      for n in range(data['N']) 
                      for s in range(data['S']) 
                      for g in range(data['G']))

# Constraints
# Capacity constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[(n, s, g)] for n in range(data['N'])) <= data['Capacity'][s][g]

# Demand constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[(n, s, g)] for s in range(data['S'])) == data['Population'][n][g]

# Solve the problem
problem.solve()

# Results
print(f'Status: {pulp.LpStatus[problem.status]}')
for n in range(data['N']):
    for s in range(data['S']):
        for g in range(data['G']):
            print(f'x[{n},{s},{g}] = {x[(n, s, g)].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')