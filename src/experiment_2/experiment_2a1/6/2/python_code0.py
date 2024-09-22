import pulp
import json

# Input data
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

# Model
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"system_{i}", lowBound=0) for i in range(data['N'])]

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU_Constraint"

# Disk drives constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"

# Memory boards constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i] - data['Preorder'][i], f"Demand_Constraint_{i}"

# GP and WS demand limits
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"

# Solve problem
problem.solve()

# Collect results
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": data['MemoryBoards'][i] * pulp.value(x[i]),
        "total_alt_boards_used": min(data['AltMemory'], x[i]) if data['AltCompatible'][i] else 0,
        "total_disk_drives_used": data['DiskDrives'][i] * pulp.value(x[i])
    })

# Calculate total profit
total_profit = pulp.value(problem.objective)

# Output
output = {
    "system_output": system_output,
    "profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')