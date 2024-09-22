import pulp
import json

data = {
    "N": 5,
    "IsWorkstation": [False, False, False, True, True],
    "Price": [60000, 40000, 30000, 30000, 15000],
    "DiskDrives": [0.3, 1.7, 0, 1.4, 0],
    "MemoryBoards": [4, 2, 2, 2, 1],
    "Demand": [1800, 999999, 300, 999999, 999999],
    "Preorder": [0, 500, 0, 500, 400],
    "AltCompatible": [True, False, False, False, False],
    "MaxCpu": 7000,
    "MinDisk": 3000,
    "MaxDisk": 7000,
    "MinMemory": 8000,
    "MaxMemory": 16000,
    "DemandGP": 3800,
    "DemandWS": 3200,
    "AltMemory": 4000
}

# Extract data from JSON
N = data['N']
is_ws = data['IsWorkstation']
prices = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
demands = data['Demand']
preorders = data['Preorder']
alt_compatible = data['AltCompatible']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_memory = data['AltMemory']

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"num_systems_{i}", lowBound=0, cat='Continuous') for i in range(N)]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0, cat='Continuous') for i in range(N)]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used_{i}", lowBound=0, cat='Continuous') for i in range(N)]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
profit = pulp.lpSum([prices[i] * x[i] for i in range(N)])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= max_cpu

# Disk constraints
problem += pulp.lpSum(disk_used) >= min_disk
problem += pulp.lpSum(disk_used) <= max_disk

# Memory constraints
problem += pulp.lpSum(mem_used) + pulp.lpSum(alt_mem_used) >= min_mem
problem += pulp.lpSum(mem_used) + pulp.lpSum(alt_mem_used) <= max_mem

# Demand and preorder constraints
for i in range(N):
    problem += x[i] <= demands[i]
    problem += x[i] >= preorders[i]

# General purpose and workstation demand constraints
problem += pulp.lpSum([x[i] for i in range(N) if not is_ws[i]]) <= demand_gp
problem += pulp.lpSum([x[i] for i in range(N) if is_ws[i]]) <= demand_ws

# Memory board usage constraints
for i in range(N):
    problem += mem_used[i] == x[i] * memory_boards[i]
    if alt_compatible[i]:
        problem += mem_used[i] + alt_mem_used[i] == x[i] * memory_boards[i]
    else:
        problem += alt_mem_used[i] == 0

# Alternative memory board constraint
problem += pulp.lpSum(alt_mem_used) <= alt_memory

# Disk drive usage constraints
for i in range(N):
    problem += disk_used[i] == x[i] * disk_drives[i]

# Solve the problem
problem.solve()

# Prepare output
system_output = [
    {
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": pulp.value(mem_used[i]),
        "total_alt_boards_used": pulp.value(alt_mem_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    }
    for i in range(N)
]

profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')