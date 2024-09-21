import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Constants
P = len(data['supply'])
C = len(data['demand'])

# Problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)  # Changed space to underscore

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the result
print(f"Status: {pulp.LpStatus[problem.status]}")
print("Amounts to be transmitted from power plants to cities:")
for p in range(P):
    for c in range(C):
        print(f"  From plant {p} to city {c}: {x[(p, c)].varValue} units")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')