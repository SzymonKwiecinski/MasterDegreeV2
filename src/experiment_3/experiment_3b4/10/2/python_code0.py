import pulp

# Given data
data = {
    'N': 5,
    'IsWorkstation': [False, False, False, True, True],
    'Price': [60000, 40000, 30000, 30000, 15000],
    'DiskDrives': [0.3, 1.7, 0, 1.4, 0],
    'MemoryBoards': [4, 2, 2, 2, 1],
    'Demand': [1800, 999999, 300, 999999, 999999],
    'Preorder': [0, 500, 0, 500, 400],
    'AltCompatible': [True, False, False, False, False],
    'MaxCpu': 7000,
    'MinDisk': 3000,
    'MaxDisk': 7000,
    'MinMemory': 8000,
    'MaxMemory': 16000,
    'DemandGP': 3800,
    'DemandWS': 3200,
    'AltMemory': 4000
}

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective function
profit = sum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU Supply Constraint
problem += sum(x) <= data['MaxCpu']

# Disk Drive Supply Constraint
problem += sum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += sum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# 256K Memory Board Supply Constraint
problem += sum(data['MemoryBoards'][i] * x[i] - y[i] + y[i] for i in range(data['N'])) >= data['MinMemory']
problem += sum(data['MemoryBoards'][i] * x[i] - y[i] + y[i] for i in range(data['N'])) <= data['MaxMemory']

# Demand Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
    problem += x[i] <= data['Demand'][i]

# GP and WS Family Constraints
gp_indexes = [i for i, ws in enumerate(data['IsWorkstation']) if not ws]
ws_indexes = [i for i, ws in enumerate(data['IsWorkstation']) if ws]

problem += sum(x[i] for i in gp_indexes) <= data['DemandGP']
problem += sum(x[i] for i in ws_indexes) <= data['DemandWS']

# Alternative Memory Usage Constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += y[i] <= x[i]
    else:
        problem += y[i] == 0

problem += sum(y) <= data['AltMemory']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')