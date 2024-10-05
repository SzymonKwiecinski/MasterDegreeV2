import pulp

# Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Indices
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities

# Problem
problem = pulp.LpProblem("Electricity_Distribution_Problem", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p, c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Capacity constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= data['supply'][p], f"Capacity_Constraint_Power_Plant_{p}"

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solving the Problem
problem.solve()

# Output the results
for p in range(P):
    for c in range(C):
        print(f"Electricity sent from power plant {p} to city {c}: {send[p, c].varValue} million kwh")

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')