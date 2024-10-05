import pulp
import json

# Load data
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
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective Function: Maximize profit
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU availability
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk availability
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']

# Memory board availability
total_standard_mem = pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])])
problem += total_standard_mem <= data['MaxMemory'] - pulp.lpSum(alt_mem_used)
problem += total_standard_mem >= data['MinMemory']

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

# Preorders
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]

# Demand for GP and WS systems
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# Alternative memory constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += alt_mem_used[i] <= data['AltMemory']
        problem += alt_mem_used[i] <= x[i] * data['MemoryBoards'][i]

# Solve the problem
problem.solve()

# Retrieve output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": data['MemoryBoards'][i] * x[i].varValue - alt_mem_used[i].varValue,
        "total_alt_boards_used": alt_mem_used[i].varValue,
        "total_disk_drives_used": data['DiskDrives'][i] * x[i].varValue
    })

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Output the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')