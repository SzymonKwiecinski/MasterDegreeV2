import pulp

# Data input
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)
C = len(demand)

# Problem definition
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0, cat='Continuous') for c in range(C)] for p in range(P)]

# Objective function
problem += pulp.lpSum(send[p][c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_Plant_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c], f"Demand_Constraint_City_{c}"

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "send": [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)],
    "total_cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')