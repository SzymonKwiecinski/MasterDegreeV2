import pulp

# Extract data from the provided JSON
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

# Create the Linear Programming problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=data['Preorder'][i], upBound=data['Demand'][i], cat='Continuous') for i in range(data['N'])]
y_256K = [pulp.LpVariable(f'y_256K_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y_alt = [pulp.LpVariable(f'y_alt_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
d_disk = [pulp.LpVariable(f'd_disk_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
problem += pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])

# Constraints
# 1. CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

# 2. Disk drive supply constraints
problem += pulp.lpSum(d_disk) >= data['MinDisk']
problem += pulp.lpSum(d_disk) <= data['MaxDisk']

# 3. Memory board supply constraints
problem += pulp.lpSum(y_256K) >= data['MinMemory']
problem += pulp.lpSum(y_256K) <= data['MaxMemory']

# 6. Demand for GP and WS families
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# 7. Memory boards usage
for i in range(data['N']):
    problem += y_256K[i] == data['MemoryBoards'][i] * x[i]

# 8. Alternative memory boards usage
for i in range(data['N']):
    problem += y_alt[i] <= data['AltCompatible'][i] * data['AltMemory']
problem += pulp.lpSum(y_alt) <= data['AltMemory']

# 9. Disk drive usage
for i in range(data['N']):
    problem += d_disk[i] == data['DiskDrives'][i] * x[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print decision variables to give insight into the model's outcome
for i in range(data['N']):
    print(f"System {i+1}: Produced: {x[i].varValue}, 256K Memory used: {y_256K[i].varValue}, Alt Memory used: {y_alt[i].varValue}, Disk Drives used: {d_disk[i].varValue}")