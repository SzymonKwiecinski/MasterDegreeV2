import json
import pulp

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

# Create a linear programming problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
num_produced = [pulp.LpVariable(f"num_produced_{i}", 0, None) for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum(num_produced[i] * data['Price'][i] for i in range(data['N']))
problem += profit

# Constraints
# CPU constraints
problem += pulp.lpSum(num_produced[i] for i in range(data['N'])) <= data['MaxCpu']

# Disk drives constraints
problem += pulp.lpSum(num_produced[i] * data['DiskDrives'][i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(num_produced[i] * data['DiskDrives'][i] for i in range(data['N'])) <= data['MaxDisk']

# Memory constraints
problem += pulp.lpSum(num_produced[i] * data['MemoryBoards'][i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(num_produced[i] * data['MemoryBoards'][i] for i in range(data['N'])) <= data['MaxMemory']

# Demand constraints for each system
for i in range(data['N']):
    problem += num_produced[i] <= data['Demand'][i] - data['Preorder'][i], f'Demand_Constraint_{i}'

# Demand constraints for GP and WS families
problem += pulp.lpSum(num_produced[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], 'Demand_GP_Constraint'
problem += pulp.lpSum(num_produced[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], 'Demand_WS_Constraint'

# Alternative memory constraints
problem += pulp.lpSum((num_produced[i] * data['MemoryBoards'][i]) for i in range(data['N']) if data['AltCompatible'][i]) <= data['AltMemory'], 'Alt_Memory_Constraint'

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(num_produced[i]) * data['MemoryBoards'][i],
        "total_alt_boards_used": pulp.value(num_produced[i]) * (1 if data['AltCompatible'][i] else 0),
        "total_disk_drives_used": pulp.value(num_produced[i]) * data['DiskDrives'][i]
    })

profit_value = pulp.value(problem.objective)

# Output JSON
output = {
    "system_output": system_output,
    "profit": profit_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')