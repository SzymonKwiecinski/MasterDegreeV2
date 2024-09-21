import pulp

# Parse the input data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Number of power plants (P) and cities (C)
P = len(data['supply'])
C = len(data['demand'])

# Decision variables x_pc (amount of electricity transmitted from plant p to city c)
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Initialize the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Objective function: Minimize the total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Constraints

# 1. Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

# 2. Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')