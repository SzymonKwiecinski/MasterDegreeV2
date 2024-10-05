import pulp
import json

# Given data
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Define the problem
problem = pulp.LpProblem("SchoolAssignmentProblem", pulp.LpMinimize)

# Indices
N = data['N']
S = data['S']
G = data['G']

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(1, N + 1), range(1, S + 1), range(1, G + 1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Distance'][n-1][s-1] * x[n][s][g] for n in range(1, N + 1) for s in range(1, S + 1) for g in range(1, G + 1))

# Constraints
# Capacity constraints
for s in range(1, S + 1):
    for g in range(1, G + 1):
        problem += pulp.lpSum(x[n][s][g] for n in range(1, N + 1)) <= data['Capacity'][s-1][g-1]

# Population constraints
for n in range(1, N + 1):
    for g in range(1, G + 1):
        problem += pulp.lpSum(x[n][s][g] for s in range(1, S + 1)) == data['Population'][n-1][g-1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')