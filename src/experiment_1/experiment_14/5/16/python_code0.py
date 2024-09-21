import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Constants
P = len(data['supply'])
C = len(data['demand'])

# Model
problem = pulp.LpProblem("Electricity_Distribution_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p, c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(x[p, c] for c in range(C)) <= data['supply'][p]

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(x[p, c] for p in range(P)) == data['demand'][c]

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')