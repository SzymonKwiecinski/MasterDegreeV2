import pulp
import json

# Data
data = json.loads('{"supply": [30, 25, 45], "demand": [40, 60], "transmission_costs": [[14, 22], [18, 12], [10, 16]]}')
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Sets and Indices
P = range(len(supply))  # Power plants indices
C = range(len(demand))   # Cities indices

# Problem Definition
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (P, C), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in P for c in C)

# Supply Constraints
for p in P:
    problem += pulp.lpSum(send[p][c] for c in C) <= supply[p]

# Demand Constraints
for c in C:
    problem += pulp.lpSum(send[p][c] for p in P) == demand[c]

# Solve the problem
problem.solve()

# Output results
for p in P:
    for c in C:
        print(f'Send from Power Plant {p} to City {c}: {send[p][c].varValue} million kWh')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')