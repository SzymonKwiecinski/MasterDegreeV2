import json
import pulp

# Input data from JSON format
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

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(data['N']), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum([x[i] for i in range(data['N'])]) <= data['MaxCpu'] 

# Disk drive constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

# Memory constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) >= data['MinMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) <= data['MaxMemory']

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]
for i in range(data['N']):
    if data['IsWorkstation'][i]:
        problem += pulp.lpSum([x[j] for j in range(data['N']) if data['IsWorkstation'][j]]) <= data['DemandWS']
    else:
        problem += pulp.lpSum([x[j] for j in range(data['N']) if not data['IsWorkstation'][j]]) <= data['DemandGP']

# Preorder constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": data['MemoryBoards'][i] * x[i].varValue,
        "total_alt_boards_used": data['AltCompatible'][i] * min(data['AltMemory'], x[i].varValue),  # Using alt memory if compatible
        "total_disk_drives_used": data['DiskDrives'][i] * x[i].varValue
    })

# Profit
profit_value = pulp.value(problem.objective)

# Final output
output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')