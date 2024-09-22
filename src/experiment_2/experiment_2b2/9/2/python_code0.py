import pulp
import json

# Load input data
data = {'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}

# Extract variables from data
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
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_mem = data['AltMemory']

# Initialize the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
used_mem = [pulp.LpVariable(f'mem_used_{i}', lowBound=0, cat='Continuous') for i in range(N)]
used_alt = [pulp.LpVariable(f'alt_used_{i}', lowBound=0, cat='Continuous') for i in range(N)]
used_disk = [pulp.LpVariable(f'disk_used_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective function: maximize total profit
problem += pulp.lpSum([price[i] * x[i] for i in range(N)])

# Constraints
# CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu

# Disk drives constraint
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk

# Memory boards constraint
problem += pulp.lpSum([memory_boards[i] * x[i] for i in range(N)]) >= min_mem
problem += pulp.lpSum([memory_boards[i] * x[i] for i in range(N)]) <= max_mem

# System demand constraints
for i in range(N):
    problem += x[i] <= demand[i]
    problem += x[i] >= preorder[i]
    problem += used_mem[i] == memory_boards[i] * x[i]
    problem += used_disk[i] == disk_drives[i] * x[i]
    if alt_compatible[i]:
        problem += used_alt[i] <= alt_mem

# General Purpose and Workstation demand constraints
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_GP
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_WS

# Solving the problem
problem.solve()

# Prepare output
system_output = []
for i in range(N):
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": used_mem[i].varValue,
        "total_alt_boards_used": used_alt[i].varValue,
        "total_disk_drives_used": used_disk[i].varValue
    })

profit = pulp.value(problem.objective)

output = {"system_output": system_output, "profit": profit}

# Print result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')