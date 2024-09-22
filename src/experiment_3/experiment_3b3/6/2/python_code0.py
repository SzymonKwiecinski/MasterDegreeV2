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

# Create the problem
problem = pulp.LpProblem("DEC_System_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0) for i in range(data['N'])]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0) for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0) for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu'], "CPU_Constraint"

# Disk constraint
for i in range(data['N']):
    problem += disk_used[i] == data['DiskDrives'][i] * x[i]

problem += data['MinDisk'] <= pulp.lpSum(disk_used) <= data['MaxDisk'], "Disk_Constraint"

# Memory constraint
for i in range(data['N']):
    problem += mem_used[i] == data['MemoryBoards'][i] * x[i] + data['AltCompatible'][i] * alt_used[i]

problem += data['MinMemory'] <= pulp.lpSum(mem_used) <= data['MaxMemory'], "Memory_Constraint"
problem += pulp.lpSum(alt_used) <= data['AltMemory'], "Alt_Memory_Constraint"

# Preorder constraint
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

# Demand constraint
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

# GP and WS demand constraints
GP_indices = [i for i in range(data['N']) if not data['IsWorkstation'][i]]
WS_indices = [i for i in range(data['N']) if data['IsWorkstation'][i]]

problem += pulp.lpSum(x[i] for i in GP_indices) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in WS_indices) <= data['DemandWS'], "WS_Demand_Constraint"

# Solve the problem
problem.solve()

# Output results
system_output = [{'system': i + 1, 'produced': x[i].varValue} for i in range(data['N'])]
profit_value = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')