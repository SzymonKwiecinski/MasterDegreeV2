import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extracting data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # Number of power plants
C = len(demand)  # Number of cities

# Defining the problem
problem = pulp.LpProblem("Electricity_Supply_Problem", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c]

# Solve the problem
problem.solve()

# Collecting results
result_send = [[send[p, c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Prepare output
output = {
    "send": result_send,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')

# Output result dictionary (optional, uncomment if you want to view the results)
# print(json.dumps(output))