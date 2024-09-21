import pulp

# Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Define the problem
problem = pulp.LpProblem("ElectricityDistribution", pulp.LpMinimize)

# Define indices
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities

# Decision variables
x = pulp.LpVariable.dicts("flow", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C)), "TotalTransmissionCost"

# Constraints
# 1. Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"SupplyConstraint_{p}"

# 2. Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == data['demand'][c], f"DemandConstraint_{c}"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')