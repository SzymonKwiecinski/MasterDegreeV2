import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Sets and indices
plants = range(len(data['supply']))
cities = range(len(data['demand']))

# Create the LP problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (plants, cities), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in plants for c in cities)

# Constraints
# Supply Constraint
for p in plants:
    problem += (pulp.lpSum(send[p][c] for c in cities) <= data['supply'][p], f"Supply_Constraint_Plant_{p}")

# Demand Constraint
for c in cities:
    problem += (pulp.lpSum(send[p][c] for p in plants) == data['demand'][c], f"Demand_Constraint_City_{c}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')