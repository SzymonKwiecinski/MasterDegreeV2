import pulp
import json

# Data provided in JSON format
data_json = '{"supply": [30, 25, 45], "demand": [40, 60], "transmission_costs": [[14, 22], [18, 12], [10, 16]]}'
data = json.loads(data_json)

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities
supply = data['supply']   # Capacity of power plants
demand = data['demand']    # Peak demand of cities
transmission_costs = data['transmission_costs']  # Transmission costs

# Problem Definition
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output results
result = {f'send_{p}_{c}': send[p][c].varValue for p in range(P) for c in range(C)}
total_cost = pulp.value(problem.objective)

print(f'Results: {result}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')