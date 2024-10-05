import pulp
import json

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
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Variables
num_produced = [pulp.LpVariable(f"x_{i}", data['Preorder'][i], data['Demand'][i]) for i in range(data['N'])]
alt_memory_used = [pulp.LpVariable(f"alt_mem_{i}", 0, data['AltMemory'] if data['AltCompatible'][i] else 0) for i in range(data['N'])]

# Objective function
profit = pulp.lpSum([num_produced[i] * data['Price'][i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(num_produced) <= data['MaxCpu']

# Disk constraints
total_disk = pulp.lpSum([num_produced[i] * data['DiskDrives'][i] for i in range(data['N'])])
problem += total_disk >= data['MinDisk']
problem += total_disk <= data['MaxDisk']

# Memory constraints
total_memory = pulp.lpSum([num_produced[i] * data['MemoryBoards'][i] - alt_memory_used[i] for i in range(data['N'])])
problem += total_memory >= data['MinMemory']
problem += total_memory <= data['MaxMemory']

# Alternative memory constraint
problem += pulp.lpSum(alt_memory_used) <= data['AltMemory']

# Demand constraints for GP and WS families
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# Solve the problem
problem.solve()

# Output
system_output = []
for i in range(data['N']):
    xi = num_produced[i].varValue
    alt_used = alt_memory_used[i].varValue
    mem_used = xi * data['MemoryBoards'][i] - alt_used
    disk_used = xi * data['DiskDrives'][i]
    system_output.append({
        "num_produced": xi,
        "total_256K_boards_used": mem_used,
        "total_alt_boards_used": alt_used,
        "total_disk_drives_used": disk_used
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')