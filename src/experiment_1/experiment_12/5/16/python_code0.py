import pulp

# Given data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Initialize the LP problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')