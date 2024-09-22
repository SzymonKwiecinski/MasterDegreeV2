import pulp

# Data input
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # number of power plants
C = len(demand)  # number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0) for c in range(C)] for p in range(P)]

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(send[p][c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == demand[c]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "send": [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')