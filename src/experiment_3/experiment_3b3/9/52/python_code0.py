import pulp

# Data
data = {
    'supply': [30, 25, 45], 
    'demand': [40, 60], 
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)   # Number of power plants
C = len(demand)   # Number of cities

# Define the problem
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

# Define decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')