import pulp

# Data from JSON format
data = {
    'supply': [30, 25, 45],  # supply capacities of power plants
    'demand': [40, 60],      # peak demands of cities
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]  # transmission costs from plants to cities
}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_P{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_C{c}"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    for c in range(C):
        print(f'Amount of electricity sent from power plant {p} to city {c}: {send[(p, c)].varValue} million kwh')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')