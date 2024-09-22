import pulp

# Parse data
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

# Define the Linear Programming problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk drive constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

# Memory constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - alt_mem_used[i] for i in range(data['N'])]) >= data['MinMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - alt_mem_used[i] for i in range(data['N'])]) <= data['MaxMemory']
# Alternative Memory constraints
problem += pulp.lpSum(alt_mem_used) <= data['AltMemory']

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]
    problem += x[i] >= data['Preorder'][i]

# GP and WS demand constraints
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# Alternative memory compatibility constraints
for i in range(data['N']):
    if not data['AltCompatible'][i]:
        problem += alt_mem_used[i] == 0

# Solve the problem
problem.solve()

# Prepare and print the output
system_output = []
for i in range(data['N']):
    num_produced = pulp.value(x[i])
    total_256K_boards_used = pulp.value(data['MemoryBoards'][i] * x[i] - alt_mem_used[i])
    total_alt_boards_used = pulp.value(alt_mem_used[i])
    total_disk_drives_used = pulp.value(data['DiskDrives'][i] * x[i])
    
    system_output.append({
        "num_produced": num_produced,
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')