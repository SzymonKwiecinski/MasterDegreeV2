import pulp

# Data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Problem
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

# Decision variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0) for c in range(C)] for p in range(P)]

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f'Supply_Constraint_{p}'

for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f'Demand_Constraint_{c}'

# Solve
problem.solve()

# Output
send_output = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_output,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')