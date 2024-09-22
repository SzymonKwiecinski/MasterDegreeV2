import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extracting data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants and cities
P = len(supply)
C = len(demand)

# LP Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", [(p, c) for p in range(P) for c in range(C)], lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_p{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_c{c}"

# Solve the problem
problem.solve()

# Prepare results
result_send = [[send[(p, c)].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "send": result_send,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')