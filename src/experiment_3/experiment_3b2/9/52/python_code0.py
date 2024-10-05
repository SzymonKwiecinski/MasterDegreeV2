import pulp

# Data input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Create the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

# Constraints 
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')