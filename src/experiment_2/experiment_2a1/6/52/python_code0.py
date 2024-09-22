import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Problem setup
P = len(data['supply'])
C = len(data['demand'])
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective function: minimize total transmission cost
problem += pulp.lpSum(send[p][c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Collecting the results
send_result = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output result
result = {
    "send": send_result,
    "total_cost": total_cost
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')