import pulp
import json

# Problem Description
problem = pulp.LpProblem("Maximize_Profit_DEC", pulp.LpMaximize)

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

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_memory_used = [pulp.LpVariable(f'alt_mem_used_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Constraints
problem += pulp.lpSum(x) <= data['MaxCpu']

problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']

problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - alt_memory_used[i] for i in range(data['N'])]) <= data['MaxMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] - alt_memory_used[i] for i in range(data['N'])]) >= data['MinMemory']

problem += pulp.lpSum([x[i] for i, is_ws in enumerate(data['IsWorkstation']) if not is_ws]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i, is_ws in enumerate(data['IsWorkstation']) if is_ws]) <= data['DemandWS']

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
    problem += x[i] <= data['Demand'][i]

for i in range(data['N']):
    if not data['AltCompatible'][i]:
        problem += alt_memory_used[i] == 0

problem += pulp.lpSum(alt_memory_used) <= data['AltMemory']

# Objective Function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Solve
problem.solve()

# Output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": data['MemoryBoards'][i] * x[i].varValue - alt_memory_used[i].varValue,
        "total_alt_boards_used": alt_memory_used[i].varValue,
        "total_disk_drives_used": data['DiskDrives'][i] * x[i].varValue
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')