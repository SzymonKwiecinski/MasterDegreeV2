import pulp

# Parse the input data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)
C = len(demand)

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Electric_Utility_Cost_Minimization", pulp.LpMinimize)

# Decision variables: Electricity sent from power plant p to city c
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize the total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Constraints
# 1. Each power plant's supply constraint
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p]

# 2. Each city's demand constraint
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Organize the output
result = {
    "send": [[pulp.value(send[(p, c)]) for c in range(C)] for p in range(P)],
    "total_cost": pulp.value(problem.objective)
}

# Print the results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')