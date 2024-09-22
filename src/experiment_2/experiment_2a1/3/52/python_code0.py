import pulp
import json

data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extract data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # number of power plants
C = len(demand)  # number of cities

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare the output
send_result = [[send[p][c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output result
output = {
    "send": send_result,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')