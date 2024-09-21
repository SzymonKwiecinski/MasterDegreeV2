import pulp

# Data from JSON format
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Constants
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities

# Define the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Constraints
# 1. Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p]

# 2. Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for p in range(P):
    for c in range(C):
        print(f'Electricity transmitted from power plant {p} to city {c}: {x[(p, c)].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')