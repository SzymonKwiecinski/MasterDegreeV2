import pulp
import json

# Load data
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

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
min_memory = data['MinMemory']
max_memory = data['MaxMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_memory = data['AltMemory']

# Initialize the optimization problem
problem = pulp.LpProblem("DEC_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x{i}", lowBound=0) for i in range(N)]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0) for i in range(N)]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0) for i in range(N)]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0) for i in range(N)]

# Objective function
profit = pulp.lpSum(price[i] * x[i] for i in range(N))
problem += profit

# Constraints
# CPU constraints
problem += pulp.lpSum(x) <= max_cpu

# Disk drive constraints
problem += pulp.lpSum(disk_used) >= min_disk
problem += pulp.lpSum(disk_used) <= max_disk

# Memory board constraints
problem += pulp.lpSum(mem_used) >= min_memory
problem += pulp.lpSum(mem_used) <= max_memory

# Memory board per system constraints
for i in range(N):
    problem += mem_used[i] + alt_used[i] == memory_boards[i] * x[i]
    if alt_compatible[i]:
        problem += alt_used[i] <= alt_memory

# Disk drives per system constraints
for i in range(N):
    problem += disk_used[i] == disk_drives[i] * x[i]

# Preorder constraints
for i in range(N):
    problem += x[i] >= preorder[i]

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i]

# GP and WS demand constraints
gp_indices = [i for i in range(N) if not is_workstation[i]]
ws_indices = [i for i in range(N) if is_workstation[i]]

problem += pulp.lpSum(x[i] for i in gp_indices) <= demand_GP
problem += pulp.lpSum(x[i] for i in ws_indices) <= demand_WS

# Solve the problem
problem.solve()

# Generate output
system_output = [{
    "num_produced": x[i].varValue,
    "total_256K_boards_used": mem_used[i].varValue,
    "total_alt_boards_used": alt_used[i].varValue,
    "total_disk_drives_used": disk_used[i].varValue
} for i in range(N)]

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')