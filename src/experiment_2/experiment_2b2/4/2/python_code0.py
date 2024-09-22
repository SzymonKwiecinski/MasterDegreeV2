import pulp

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

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_produced = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
mem_used_256k = [pulp.LpVariable(f"mem_used_256k_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
profit = pulp.lpSum(data['Price'][i] * num_produced[i] for i in range(data['N']))
problem += profit

# Constraints

# CPU constraints
problem += pulp.lpSum(num_produced) <= data['MaxCpu'], "CPU_Constraint"

# Disk drive constraints
problem += pulp.lpSum(data['DiskDrives'][i] * num_produced[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * num_produced[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"

# 256K memory board constraints
problem += pulp.lpSum(mem_used_256k) >= data['MinMemory'], "Min_Mem_Constraint_256k"
problem += pulp.lpSum(mem_used_256k) <= data['MaxMemory'], "Max_Mem_Constraint_256k"

# Alternative memory board constraints
problem += pulp.lpSum(alt_mem_used) <= data['AltMemory'], "Alt_Mem_Constraint"

# Demand constraints
for i in range(data['N']):
    problem += num_produced[i] <= data['Demand'][i], f"Demand_Constraint_{i}"
    problem += mem_used_256k[i] + alt_mem_used[i] == data['MemoryBoards'][i] * num_produced[i], f"Mem_Board_Usage_{i}"
    problem += disk_used[i] == data['DiskDrives'][i] * num_produced[i], f"Disk_Drive_Usage_{i}"
    # AltMemory are used only if compatible
    if not data['AltCompatible'][i]:
        problem += alt_mem_used[i] == 0, f"Alt_Mem_Usage_{i}"

# Demand constraints for GP and WS
gp_indices = [i for i in range(data['N']) if not data['IsWorkstation'][i]]
ws_indices = [i for i in range(data['N']) if data['IsWorkstation'][i]]

problem += pulp.lpSum(num_produced[i] for i in gp_indices) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(num_produced[i] for i in ws_indices) <= data['DemandWS'], "WS_Demand_Constraint"

# Preorders constraints
for i in range(data['N']):
    problem += num_produced[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

# Solve problem
problem.solve()

# Output result
system_output = [
    {
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(mem_used_256k[i]),
        "total_alt_boards_used": pulp.value(alt_mem_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    }
    for i in range(data['N'])
]

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')