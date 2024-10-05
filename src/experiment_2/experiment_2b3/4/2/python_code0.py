import pulp

# Problem data
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

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used{i}", lowBound=0) for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used{i}", lowBound=0) for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used{i}", lowBound=0) for i in range(data['N'])]

# Objective function: maximize profit
total_profit = pulp.lpSum([
    x[i] * data['Price'][i] for i in range(data['N'])
])
problem += total_profit

# Constraints
# Demand constraints for each system
for i in range(data['N']):
    problem += (x[i] <= data['Demand'][i], f"Demand_constraint_{i}")
    problem += (x[i] >= data['Preorder'][i], f"Preorder_constraint_{i}")

# CPU constraint
problem += (pulp.lpSum(x) <= data['MaxCpu'], "CPU_supply_constraint")

# Memory constraints
total_mem_used = pulp.lpSum([
    x[i] * data['MemoryBoards'][i] for i in range(data['N'])
])
problem += (total_mem_used >= data['MinMemory'], "Min_memory_constraint")
problem += (total_mem_used <= data['MaxMemory'], "Max_memory_constraint")

# Alternative memory use constraint
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += (alt_mem_used[i] <= data['AltMemory'], f"Alt_memory_constraint_{i}")
    else:
        problem += (alt_mem_used[i] == 0, f"Alt_memory_constraint_{i}_not_compatible")

# Disk drive constraints
total_disk_used = pulp.lpSum([
    x[i] * data['DiskDrives'][i] for i in range(data['N'])
])
problem += (total_disk_used >= data['MinDisk'], "Min_disk_constraint")
problem += (total_disk_used <= data['MaxDisk'], "Max_disk_constraint")

# GP demand constraint
total_GP = pulp.lpSum([
    x[i] for i in range(data['N']) if not data['IsWorkstation'][i]
])
problem += (total_GP <= data['DemandGP'], "GP_demand_constraint")

# WS demand constraint
total_WS = pulp.lpSum([
    x[i] for i in range(data['N']) if data['IsWorkstation'][i]
])
problem += (total_WS <= data['DemandWS'], "WS_demand_constraint")

# Solve problem
problem.solve()

# Prepare output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": pulp.value(mem_used[i]),
        "total_alt_boards_used": pulp.value(alt_mem_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(total_profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')