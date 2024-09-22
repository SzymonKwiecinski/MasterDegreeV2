import pulp

# Data
data = {
    'S': 3,  # Number of schools
    'G': 2,  # Number of grades
    'N': 4,  # Number of neighborhoods
    'Capacity': [[15, 20], [20, 15], [5, 17]],  # Capacity of schools for each grade
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],  # Student population in neighborhoods for each grade
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]  # Distance from each neighborhood to each school
}

# Problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[(n, s, g)] for n in range(data['N']) for s in range(data['S']) for g in range(data['G']))

# Constraints
# Capacity Constraints
for s in range(data['S']):
    problem += (pulp.lpSum(x[(n, s, g)] for n in range(data['N']) for g in range(data['G'])) <= sum(data['Capacity'][s][g] for g in range(data['G'])))

# Population Constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += (pulp.lpSum(x[(n, s, g)] for s in range(data['S'])) == data['Population'][n][g])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')