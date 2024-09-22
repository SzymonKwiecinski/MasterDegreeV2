import pulp

# Data from the problem
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables: amount of electricity power plant p sends to city c
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Constraints
# 1. Supply constraints: Each plant cannot send more than its capacity
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= data['supply'][p]

# 2. Demand constraints: Each city's demand must be met
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Prepare the solution in the desired format
send_solution = [
    [pulp.value(send[(p, c)]) for c in range(C)] 
    for p in range(P)
]

output = {
    "send": send_solution,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')