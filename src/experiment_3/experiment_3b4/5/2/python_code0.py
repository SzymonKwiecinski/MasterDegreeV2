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

# Decision variables
x = [pulp.LpVariable(f"x_{i}", cat='Continuous') for i in range(data['N'])]
a = [pulp.LpVariable(f"a_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
problem += pulp.lpSum(x) <= data['MaxCpu'], "CPU_constraint"
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk'], "Max_disk_constraint"
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk'], "Min_disk_constraint"
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - a[i] for i in range(data['N'])]) <= data['MaxMemory'], "Max_memory_constraint"
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - a[i] for i in range(data['N'])]) >= data['MinMemory'], "Min_memory_constraint"
problem += pulp.lpSum(a) <= data['AltMemory'], "Alt_memory_constraint"

for i in range(data['N']):
    problem += a[i] <= data['AltCompatible'][i] * data['MemoryBoards'][i] * x[i], f"Alt_memory_compatible_{i}"
    problem += x[i] <= data['Demand'][i], f"Demand_constraint_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_constraint_{i}"

problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP'], "Demand_GP_constraint"
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS'], "Demand_WS_constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')