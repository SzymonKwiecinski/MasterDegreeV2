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

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
demand = data['Demand']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_produced = [pulp.LpVariable(f'prod_{i}', lowBound=0) for i in range(N)]
alt_board_used = [pulp.LpVariable(f'alt_board_{i}', lowBound=0, cat='Integer') for i in range(N)]
disk_used = [pulp.LpVariable(f'disk_used_{i}', lowBound=0) for i in range(N)]

# Objective function
profit = pulp.lpSum(price[i] * num_produced[i] for i in range(N))
problem += profit

# Constraints
problem += pulp.lpSum(num_produced[i] for i in range(N)) <= max_cpu  # CPU constraint

# Disk constraints
problem += pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N)) >= min_disk
problem += pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N)) <= max_disk

# Memory constraints
problem += pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N)) >= min_mem
problem += pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N)) <= max_mem

# Demand constraints
for i in range(N):
    problem += num_produced[i] <= demand[i]
    problem += num_produced[i] >= preorder[i]

# Workstation and GP family constraints
problem += pulp.lpSum(num_produced[i] for i in range(N) if not is_workstation[i]) <= demand_GP
problem += pulp.lpSum(num_produced[i] for i in range(N) if is_workstation[i]) <= demand_WS

# Solve the problem
problem.solve()

# Collecting the results
system_output = []
for i in range(N):
    total_256K_boards_used = memory_boards[i] * pulp.value(num_produced[i])
    total_alt_boards_used = alt_board_used[i]
    total_disk_drives_used = disk_drives[i] * pulp.value(num_produced[i])
    system_output.append({
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

# Calculate total profit
total_profit = pulp.value(problem.objective)

# Preparing the final output
output = {
    "system_output": system_output,
    "profit": total_profit
}

# JSON output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')