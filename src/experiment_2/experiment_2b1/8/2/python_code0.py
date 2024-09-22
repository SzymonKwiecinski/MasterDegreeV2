import json
import pulp

# Data from input
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
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]

# Objective function: Maximize profit
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

# Demand Constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]  # individual demand limit

# GP Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'] 

# WS Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'] 

# Disk Drives Constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# Memory Boards Constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']

# Alternative Memory Boards Constraint
alt_used = pulp.lpSum(x[i] for i in range(data['N']) if data['AltCompatible'][i])  # Only for compatible systems
problem += alt_used <= data['AltMemory']

# Preorders Constraint
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]

# Solve the problem
problem.solve()

# Get the results
system_output = []
for i in range(data['N']):
    mem_used_i = data['MemoryBoards'][i] * x[i].varValue
    alt_used_i = x[i].varValue if data['AltCompatible'][i] else 0
    disk_used_i = data['DiskDrives'][i] * x[i].varValue
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": mem_used_i,
        "total_alt_boards_used": alt_used_i,
        "total_disk_drives_used": disk_used_i
    })

# Calculate total profit
total_profit = pulp.value(problem.objective)

# Prepare output
output = {
    "system_output": system_output,
    "profit": total_profit
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')