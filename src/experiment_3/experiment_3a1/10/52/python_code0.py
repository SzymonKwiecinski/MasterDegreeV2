import pulp

# Data from the JSON format
data = {
    'supply': [30, 25, 45], 
    'demand': [40, 60], 
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Sets
P = range(len(data['supply']))  # Power plants
C = range(len(data['demand']))   # Cities

# Create a linear programming problem
problem = pulp.LpProblem("Electricity_Transmission_Optimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (P, C), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in P for c in C), "Total_Transmission_Cost"

# Demand constraints
for c in C:
    problem += pulp.lpSum(send[p][c] for p in P) == data['demand'][c], f"Demand_Constraint_city_{c}"

# Supply constraints
for p in P:
    problem += pulp.lpSum(send[p][c] for c in C) <= data['supply'][p], f"Supply_Constraint_plant_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')