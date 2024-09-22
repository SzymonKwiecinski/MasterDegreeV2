import pulp

# Problem Data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Indices
S = range(data['S'])
G = range(data['G'])
N = range(data['N'])

# Problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in N for s in S for g in G), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[n, s, g] for n in N for s in S for g in G)

# Constraints
# Each neighborhood's student population must be fully assigned
for n in N:
    for g in G:
        problem += pulp.lpSum(x[n, s, g] for s in S) == data['Population'][n][g]

# Each school cannot exceed its capacity
for s in S:
    for g in G:
        problem += pulp.lpSum(x[n, s, g] for n in N) <= data['Capacity'][s][g]

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')