import pulp

# Data from the provided JSON format
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Transmission", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transmission costs
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p, c] for p in range(P) for c in range(C))

# Constraints

# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(x[p, c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(x[p, c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the optimized objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')