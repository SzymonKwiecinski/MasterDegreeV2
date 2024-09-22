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

# Indices
GP_indices = [i for i, is_ws in enumerate(data['IsWorkstation']) if not is_ws]
WS_indices = [i for i, is_ws in enumerate(data['IsWorkstation']) if is_ws]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data['Preorder'][i], cat='Continuous') for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])]), "Total_Profit"

# Constraints
problem += pulp.lpSum([x[i] for i in range(data['N'])]) <= data['MaxCpu'], "CPU_constraint"

problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk'], "Disk_supply_constraint"

problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) <= data['MaxMemory'], "Memory_supply_constraint"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_constraint_{i}"

problem += pulp.lpSum([x[i] for i in GP_indices]) <= data['DemandGP'], "GP_demand_constraint"

problem += pulp.lpSum([x[i] for i in WS_indices]) <= data['DemandWS'], "WS_demand_constraint"

for i in range(data['N']):
    problem += mem_used[i] <= data['MemoryBoards'][i] * x[i], f"Memory_usage_constraint_{i}"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += alt_used[i] <= data['AltMemory'], f"Alternative_memory_usage_{i}"

# Solve
problem.solve()

# Output
output = {
    "system_output": [
        {
            "num_produced": x[i].varValue,
            "total_256K_boards_used": mem_used[i].varValue,
            "total_alt_boards_used": alt_used[i].varValue,
            "total_disk_drives_used": disk_used[i].varValue,
        }
        for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')