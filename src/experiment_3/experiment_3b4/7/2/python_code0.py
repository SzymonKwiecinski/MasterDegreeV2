import pulp

# Data from the JSON
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
    problem += x[i] <= data['Demand'][i]

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N']) if data['AltCompatible'][i]) <= data['AltMemory']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')