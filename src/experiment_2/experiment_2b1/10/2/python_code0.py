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
    'AltMemory': 4000,
}

# Variables
N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_memory = data['MinMemory']
max_memory = data['MaxMemory']
demand = data['Demand']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
preorder = data['Preorder']
alt_memory = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(N)]  # Production quantities

# Constraints
problem += pulp.lpSum(x) <= max_cpu  # CPU constraint

# Disk drives constraint
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) >= min_disk, "MinDisk"
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) <= max_disk, "MaxDisk"

# Memory constraints
problem += pulp.lpSum(memory_boards[i] * x[i] for i in range(N) if not alt_compatible[i]) >= min_memory, "MinMemory"
problem += pulp.lpSum(memory_boards[i] * x[i] for i in range(N) if not alt_compatible[i]) <= max_memory, "MaxMemory"
problem += pulp.lpSum(memory_boards[i] * x[i] for i in range(N) if alt_compatible[i]) <= alt_memory, "AltMemory"

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i] - preorder[i]

# General purpose family constraint
for i in range(N):
    if not is_workstation[i]:
        problem += pulp.lpSum(x[j] for j in range(N) if not is_workstation[j]) <= demand_GP

# Workstation family constraint
for i in range(N):
    if is_workstation[i]:
        problem += pulp.lpSum(x[j] for j in range(N) if is_workstation[j]) <= demand_WS

# Objective function
profit = pulp.lpSum(price[i] * x[i] for i in range(N))
problem += profit

# Solve the problem
problem.solve()

# Output results
system_output = []
for i in range(N):
    if x[i].varValue > 0:
        total_disk_drives_used = disk_drives[i] * x[i].varValue
        total_256K_boards_used = memory_boards[i] * x[i].varValue
        total_alt_boards_used = 0  # Assuming alternative boards are not used
        system_output.append({
            "num_produced": x[i].varValue,
            "total_256K_boards_used": total_256K_boards_used,
            "total_alt_boards_used": total_alt_boards_used,
            "total_disk_drives_used": total_disk_drives_used
        })

# Compile result
result = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result in JSON format
print(json.dumps(result, indent=4))