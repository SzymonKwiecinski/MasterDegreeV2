import pulp
import json

# Data input
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Create the problem instance
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(data['N']), range(data['S']), range(data['G'])), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in range(data['N']) for s in range(data['S']) for g in range(data['G']))

# Capacity constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for n in range(data['N'])) <= data['Capacity'][s][g]

# Population constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for s in range(data['S'])) == data['Population'][n][g]

# Solve the problem
problem.solve()

# Output the assignment and total distance
assignment = {f'x_{n}_{s}_{g}': x[n][s][g].varValue for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])}
total_distance = pulp.value(problem.objective)

print("Assignments:")
for k, v in assignment.items():
    print(f"{k}: {v}")

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')