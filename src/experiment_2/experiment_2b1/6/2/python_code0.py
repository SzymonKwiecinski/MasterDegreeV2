import pulp
import json

# Data input
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

# Create the model
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Define variables
systems_produced = [
    pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])
]

# Objective function: Maximize profit
profit = pulp.lpSum(data['Price'][i] * systems_produced[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(systems_produced) <= data['MaxCpu'], "MaxCpuConstraint"

# Disk drives constraints
total_disk_drives_used = pulp.lpSum(data['DiskDrives'][i] * systems_produced[i] for i in range(data['N']))
problem += total_disk_drives_used >= data['MinDisk'], "MinDiskConstraint"
problem += total_disk_drives_used <= data['MaxDisk'], "MaxDiskConstraint"

# Memory constraints
total_memory_boards_used = pulp.lpSum(data['MemoryBoards'][i] * systems_produced[i] for i in range(data['N']))
problem += total_memory_boards_used >= data['MinMemory'], "MinMemoryConstraint"
problem += total_memory_boards_used <= data['MaxMemory'], "MaxMemoryConstraint"

# Demand constraints
for i in range(data['N']):
    problem += systems_produced[i] <= data['Demand'][i], f"DemandConstraint_{i}"

# Workstation and General Purpose constraints
problem += pulp.lpSum(systems_produced[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "MaxWSConstraint"
problem += pulp.lpSum(systems_produced[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "MaxGPConstraint"

# Preorder constraints
for i in range(data['N']):
    problem += systems_produced[i] >= data['Preorder'][i], f"PreorderConstraint_{i}"

# Solve the problem
problem.solve()

# Preparing output
system_output = []
for i in range(data['N']):
    system_output.append({
        "num_produced": pulp.value(systems_produced[i]),
        "total_256K_boards_used": pulp.value(data['MemoryBoards'][i] * systems_produced[i]),
        "total_alt_boards_used": pulp.value(0),  # Placeholder since alt boards usage is not defined in the constraints
        "total_disk_drives_used": pulp.value(data['DiskDrives'][i] * systems_produced[i])
    })

profit_value = pulp.value(problem.objective)

# Creating final output
output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print the final output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')