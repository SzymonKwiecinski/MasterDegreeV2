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

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
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

# Initialize the problem
problem = pulp.LpProblem("DEC_Production", pulp.LpMaximize)

# Decision variables
num_produced = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
total_alt_boards_used = [pulp.LpVariable(f'alt_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function: Maximize profit
profit = pulp.lpSum((price[i] * num_produced[i]) for i in range(N))
problem += profit

# Constraints

# CPU availability
problem += pulp.lpSum(num_produced[i] for i in range(N)) <= max_cpu

# Disk drive constraints
total_disk_drives = pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N))
problem += total_disk_drives >= min_disk
problem += total_disk_drives <= max_disk

# Memory board constraints
total_memory_boards = pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N))
total_standard_boards = total_memory_boards - pulp.lpSum(total_alt_boards_used[i] for i in range(N))
problem += total_standard_boards >= min_mem
problem += total_standard_boards <= max_mem

# Alternative memory constraints
for i in range(N):
    if alt_compatible[i]:
        problem += total_alt_boards_used[i] <= num_produced[i] * memory_boards[i]
    else:
        problem += total_alt_boards_used[i] == 0

# Alternative memory supply constraint
problem += pulp.lpSum(total_alt_boards_used[i] for i in range(N)) <= alt_mem

# Demand and preorder constraints
for i in range(N):
    problem += num_produced[i] >= preorder[i]
    problem += num_produced[i] <= demand[i]

# Total GP and WS demand constraints
problem += pulp.lpSum(num_produced[i] for i in range(N) if not is_workstation[i]) <= demand_gp
problem += pulp.lpSum(num_produced[i] for i in range(N) if is_workstation[i]) <= demand_ws

# Solve the problem
problem.solve()

# Prepare the output
system_output = [
    {
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(num_produced[i]) * memory_boards[i] - pulp.value(total_alt_boards_used[i]),
        "total_alt_boards_used": pulp.value(total_alt_boards_used[i]),
        "total_disk_drives_used": pulp.value(num_produced[i]) * disk_drives[i]
    }
    for i in range(N)
]

profit_value = pulp.value(profit)

output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')