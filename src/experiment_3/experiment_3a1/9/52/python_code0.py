import pulp
import json

# Data in JSON format
data = '''{
    "supply": [30, 25, 45],
    "demand": [40, 60],
    "transmission_costs": [[14, 22], [18, 12], [10, 16]]
}'''
data = json.loads(data)

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("Power_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the results
send_values = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print(f' (Sent Electricity): {send_values}')