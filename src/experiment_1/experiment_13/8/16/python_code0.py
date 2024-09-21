import pulp

# Data from the provided JSON format
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Constants
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Create the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables: x_pc
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints: Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Capacity_Plant_{p}"

# Constraints: Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_City_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')