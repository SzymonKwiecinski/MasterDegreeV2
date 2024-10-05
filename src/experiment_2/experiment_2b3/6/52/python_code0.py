import pulp

# Define the data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Extract values from the data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the number of power plants and cities
P = len(supply)
C = len(demand)

# Initialize the optimization problem
problem = pulp.LpProblem("Electric_Utility", pulp.LpMinimize)

# Define decision variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0) for c in range(C)] for p in range(P)]

# Define the objective function
problem += pulp.lpSum(send[p][c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Define the supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Define the demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Construct the output
output = {
    "send": [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')