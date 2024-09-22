import pulp
import json

# Given data
data_json = '''{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}'''
data = json.loads(data_json)

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Create the problem
problem = pulp.LpProblem("Power_Distribution", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output results
send_values = {f'send_{p}_{c}': send[p, c].varValue for p in range(P) for c in range(C)}
total_cost = pulp.value(problem.objective)

print("Send Values:")
for key, value in send_values.items():
    print(f"{key}: {value}")

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')