import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Sets
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities

# Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Constraints
# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')