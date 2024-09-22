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

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Problem
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Constraints

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p]

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    for c in range(C):
        print(f"Power Plant {p} to City {c}: {send[(p, c)].varValue} million kwh")

print(f'Total Transmission Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')