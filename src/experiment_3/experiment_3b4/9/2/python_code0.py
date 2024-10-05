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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
m = [pulp.LpVariable(f"m_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
a = [pulp.LpVariable(f"a_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
d = [pulp.LpVariable(f"d_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total Profit"

# Constraints
# CPU constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU Constraint"

# Disk constraints
problem += pulp.lpSum(d[i] for i in range(data['N'])) <= data['MaxDisk'], "Max Disk Constraint"
problem += pulp.lpSum(d[i] for i in range(data['N'])) >= data['MinDisk'], "Min Disk Constraint"

# Memory constraints
problem += pulp.lpSum(m[i] for i in range(data['N'])) <= data['MaxMemory'], "Max 256K Memory Constraint"
problem += pulp.lpSum(m[i] for i in range(data['N'])) >= data['MinMemory'], "Min 256K Memory Constraint"

# Alternative memory constraint
problem += pulp.lpSum(a[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative Memory Constraint"

# Memory and disk drives requirements
for i in range(data['N']):
    problem += m[i] + a[i] == data['MemoryBoards'][i] * x[i], f"Memory Requirement for System {i}"
    problem += d[i] == data['DiskDrives'][i] * x[i], f"Disk Requirement for System {i}"

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Max Demand for System {i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder Demand for System {i}"

# GP and WS constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP System Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS System Constraint"

# Alternative compatibility constraint
for i in range(data['N']):
    problem += a[i] <= data['AltCompatible'][i] * x[i], f"Alt Memory Compatibility for System {i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')