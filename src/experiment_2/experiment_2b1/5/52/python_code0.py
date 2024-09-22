import pulp
import json

# Load data from JSON
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Parameters
P = len(data['supply'])  # number of power plants
C = len(data['demand'])   # number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Transmission_Optimization", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare the output
send_result = [[pulp.value(send[(p, c)]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Display the result
output = {
    "send": send_result,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')