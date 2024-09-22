import pulp

# Data
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

# Cost related data (assumed as provided independently)
cost_memory = [2000, 1200, 1000, 1000, 500]  # Hypothetical costs for memory boards
cost_disk = [500, 1000, 1500, 2000, 2500]    # Hypothetical costs for disk drives

# Problem Definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=data['Preorder'][i], cat='Integer') for i in range(data['N'])]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum(
    data['Price'][i] * x[i] 
    - cost_memory[i] * (data['MemoryBoards'][i] * x[i] - y[i]) 
    - cost_disk[i] * data['DiskDrives'][i] * x[i]
    for i in range(data['N'])
)
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

# Disk Drive Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# Memory Board Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']

# Demand and Preorder Constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']

# Alternative Memory Constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += y[i] <= data['AltMemory']

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')