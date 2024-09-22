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

# Problem setup
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables
num_produced = [pulp.LpVariable(f'num_produced_{i}', lowBound=0) for i in range(data['N'])]

# Objective function
profit = pulp.lpSum([data['Price'][i] * num_produced[i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum([num_produced[i] for i in range(data['N'])]) <= data['MaxCpu']

# Disk drive constraints
disk_used = pulp.lpSum([data['DiskDrives'][i] * num_produced[i] for i in range(data['N'])])
problem += disk_used >= data['MinDisk']
problem += disk_used <= data['MaxDisk']

# Memory constraints
mem_used = pulp.lpSum([data['MemoryBoards'][i] * num_produced[i] for i in range(data['N'])])
problem += mem_used >= data['MinMemory']
problem += mem_used <= data['MaxMemory']

# Demand constraints for each system
for i in range(data['N']):
    problem += num_produced[i] <= data['Demand'][i]

# Demand constraints for GP and WS families
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']

# Preorder constraints
for i in range(data['N']):
    problem += num_produced[i] >= data['Preorder'][i]

# Solve the problem
problem.solve()

# Output preparation
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": num_produced[i].varValue,
        "total_256K_boards_used": data['MemoryBoards'][i] * num_produced[i].varValue,
        "total_alt_boards_used": (data['AltCompatible'][i] * data['AltMemory'] if data['AltCompatible'][i] else 0),
        "total_disk_drives_used": data['DiskDrives'][i] * num_produced[i].varValue
    })

profit_value = pulp.value(problem.objective)

# Final output
output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print the objective value
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')

# The output is prepared in the specified format
print(json.dumps(output, indent=4))