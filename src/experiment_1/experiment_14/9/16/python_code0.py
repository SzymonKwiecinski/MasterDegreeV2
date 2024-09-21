import pulp

# Data from the JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transmission costs
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Constraints
# Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p]

# Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')