import pulp
import json

# Provided data
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

# Extracting variables
N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
mem_boards = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_compatible = data['AltCompatible']

max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_mem = data['AltMemory']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=preorder[i], upBound=demand[i]) for i in range(N)]

# Objective function
profit = pulp.lpSum([price[i] * x[i] for i in range(N)])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu

# Disk drive constraints
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk

# Memory board constraints
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) <= max_mem
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) >= min_mem

# GP and WS demand constraints
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws

# Alternative memory constraints
problem += pulp.lpSum([alt_compatible[i] * x[i] for i in range(N)]) <= alt_mem

# Solve the problem
problem.solve()

# Prepare output
output = {
    "system_output": [],
    "profit": pulp.value(problem.objective)
}

for i in range(N):
    num_produced = pulp.value(x[i])
    total_256K_boards_used = mem_boards[i] * num_produced
    total_alt_boards_used = alt_compatible[i] * num_produced if alt_compatible[i] else 0
    total_disk_drives_used = disk_drives[i] * num_produced

    output["system_output"].append({
        "num_produced": num_produced,
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')