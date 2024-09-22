import pulp
import json

# Data
data = json.loads('{"supply": [30, 25, 45], "demand": [40, 60], "transmission_costs": [[14, 22], [18, 12], [10, 16]]}')
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Problem Definition
problem = pulp.LpProblem("Electric_Utility_Optimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_for_Plant_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_for_City_{c}"

# Solve the problem
problem.solve()

# Output the results
sends = {(p, c): send[(p, c)].varValue for p in range(P) for c in range(C)}
total_cost = pulp.value(problem.objective)

print(f'Supply from each power plant to each city: {sends}')
print(f'Total Transmission Cost: <OBJ>{total_cost}</OBJ>')