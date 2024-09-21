import pulp

# Data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Problem
problem = pulp.LpProblem("SchoolAssignmentProblem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(data['N']) for g in range(data['G']) for s in range(data['S'])),
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[n, g, s] for n in range(data['N']) for g in range(data['G']) for s in range(data['S']))

# Constraints
# Constraint (1): Total number of students from each student group g assigned from neighborhood n to schools
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for s in range(data['S'])) <= data['Population'][n][g]

# Constraint (2): Total number of students from each student group g assigned to school s
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for n in range(data['N'])) <= data['Capacity'][s][g]

# Constraint (3): Each student is assigned to exactly one school
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n, g, s] for s in range(data['S'])) == data['Population'][n][g]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')