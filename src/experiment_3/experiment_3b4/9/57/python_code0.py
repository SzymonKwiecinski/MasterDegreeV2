import pulp

# Data extracted from the provided JSON
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

# Create the problem
problem = pulp.LpProblem("Container_Yard_Optimization", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{t}', lowBound=0, cat='Integer') for t in range(data['T'])]
y = [pulp.LpVariable(f'y_{t}', lowBound=0, cat='Integer') for t in range(data['T'])]
s = [pulp.LpVariable(f's_{t}', lowBound=0, cat='Integer') for t in range(data['T'] + 1)]

# Objective function
problem += pulp.lpSum(
    data['UnloadCosts'][t] * x[t] + data['HoldingCost'] * s[t + 1] + data['CraneCost'] * y[t]
    for t in range(data['T'])
)

# Constraints
problem += (s[0] == data['InitContainer'])  # Initial containers

for t in range(data['T']):
    problem += (x[t] <= data['UnloadCapacity'][t])  # Unloading capacity
    problem += (y[t] <= data['NumCranes'])  # Maximum cranes
    problem += (s[t + 1] <= data['MaxContainer'])  # Storage limitation
    problem += (y[t] * data['CraneCapacity'] >= data['Demands'][t])  # Crane capacity
    problem += (s[t] + x[t] - data['Demands'][t] == s[t + 1])  # Demand satisfaction

problem += (s[data['T']] == 0)  # Ending storage

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')