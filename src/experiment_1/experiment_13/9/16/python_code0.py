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

# Create the Linear Programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables: amount of electricity transmitted from power plant p to city c
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# 1. Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# 2. Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')