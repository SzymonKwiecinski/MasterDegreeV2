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

# Define the problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f'alt_mem_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraints
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk drive supply constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

# Memory board constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) + \
           pulp.lpSum(alt_mem_used) <= data['MaxMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) + \
           pulp.lpSum(alt_mem_used) >= data['MinMemory']

# Alternative memory constraint
problem += pulp.lpSum(alt_mem_used) <= data['AltMemory']

# Max demand constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]  # Fulfill preorders
    problem += x[i] <= data['Demand'][i]    # Do not exceed individual demand

# GP and WS family demand
gp_demand = pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]])
ws_demand = pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]])
problem += gp_demand <= data['DemandGP']
problem += ws_demand <= data['DemandWS']

# Alternative memory compatibility constraint
for i in range(data['N']):
    if not data['AltCompatible'][i]:
        problem += alt_mem_used[i] == 0
    else:
        problem += alt_mem_used[i] <= data['MemoryBoards'][i] * x[i]

# Solve the problem
problem.solve()

# Output the results
system_output = []
for i in range(data['N']):
    num_produced = pulp.value(x[i])
    mem_used = num_produced * data['MemoryBoards'][i]
    alt_used = pulp.value(alt_mem_used[i])
    disk_used = num_produced * data['DiskDrives'][i]
    system_output.append({
        "num_produced": num_produced,
        "total_256K_boards_used": mem_used,
        "total_alt_boards_used": alt_used,
        "total_disk_drives_used": disk_used
    })

profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)