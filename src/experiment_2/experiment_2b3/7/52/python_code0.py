import pulp

# Problem data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Indices
P = len(supply)
C = len(demand)

# Define the problem
problem = pulp.LpProblem("Power_Plant_Distribution", pulp.LpMinimize)

# Decision variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0) for c in range(C)] for p in range(P)]

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints (each plant cannot send more electricity than it can produce)
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand constraints (each city must receive enough electricity to meet its demand)
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c]

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "send": [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)],
    "total_cost": pulp.value(problem.objective)
}

print(f"Output: {output}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")