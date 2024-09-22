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

# Creating the LP problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), 0)

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c]

# Solve the problem
problem.solve()

# Prepare the output
send_result = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output final results
output = {
    "send": send_result,
    "total_cost": total_cost
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')