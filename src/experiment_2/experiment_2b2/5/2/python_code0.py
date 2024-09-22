import pulp
import json

# Load the input data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data['Preorder'][i], cat='Continuous') for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk drive constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

# Memory board constraints
problem += pulp.lpSum(mem_used) >= data['MinMemory']
problem += pulp.lpSum(mem_used) <= data['MaxMemory']

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

# Family constraints
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# Memory board usage constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += data['MemoryBoards'][i] * x[i] == mem_used[i] + alt_used[i]
        problem += alt_used[i] <= data['AltMemory']
    else:
        problem += data['MemoryBoards'][i] * x[i] == mem_used[i]

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": pulp.value(mem_used[i]),
        "total_alt_boards_used": pulp.value(alt_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Print Output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')