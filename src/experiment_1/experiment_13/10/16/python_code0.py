import pulp

# Data from the provided JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Define the number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create the Linear Programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')