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

# Initialize the problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Sets and indices
N = range(data['N'])  # Neighborhoods
S = range(data['S'])  # Schools
G = range(data['G'])  # Grades

# Decision variables
x = pulp.LpVariable.dicts("x", (N, S, G), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in N for s in S for g in G)

# Constraints

# All students are assigned
for n in N:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for s in S) == data['Population'][n][g]

# Respect school capacities
for s in S:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for n in N) <= data['Capacity'][s][g]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')