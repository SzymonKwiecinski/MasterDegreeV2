import json
import pulp

data = {'supply': [30, 25, 45], 
        'demand': [40, 60], 
        'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extracting data from JSON
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # Number of power plants
C = len(demand)  # Number of cities

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Create decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Preparing the output
result_send = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "send": result_send,
    "total_cost": total_cost
}

# Print statement for objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')

# For display, you can print the final output dictionary
print(json.dumps(output, indent=4))