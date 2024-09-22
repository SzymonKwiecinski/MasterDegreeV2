import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supplies = data['supply']
demands = data['demand']
transmission_costs = data['transmission_costs']

P = len(supplies)
C = len(demands)

# Define the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supplies[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) == demands[c]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')