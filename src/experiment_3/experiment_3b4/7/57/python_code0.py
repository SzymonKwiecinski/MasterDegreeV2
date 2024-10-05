import pulp

# Data
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Create a linear programming problem
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=0, upBound=data['UnloadCapacity'][t], cat='Integer') for t in range(data['T'])]
y = [pulp.LpVariable(f'y_{t}', lowBound=0, upBound=data['MaxContainer'], cat='Integer') for t in range(data['T'] + 1)]
z = [pulp.LpVariable(f'z_{t}', lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]

# Objective function
problem += pulp.lpSum([
    data['UnloadCosts'][t] * x[t] + data['HoldingCost'] * y[t + 1] + data['CraneCost'] * z[t]
    for t in range(data['T'])
])

# Constraints

# Initial container condition
problem += (y[0] == data['InitContainer'], "Initial_Condition")

# Flow balance constraints
for t in range(data['T']):
    problem += (y[t + 1] == y[t] + x[t] - data['Demands'][t], f"Flow_Balance_{t}")

# Final condition
problem += (y[data['T']] == 0, "Final_Condition")

# Crane constraints
for t in range(data['T']):
    problem += (z[t] * data['CraneCapacity'] >= data['Demands'][t], f"Cranes_Demand_{t}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')