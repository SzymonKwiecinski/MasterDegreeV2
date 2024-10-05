import pulp

# Data from the input
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

# Extracting data
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

# Problem definition
problem = pulp.LpProblem("DEC_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(N)]
u_256 = [pulp.LpVariable(f"u_256_{i}", lowBound=0, cat='Continuous') for i in range(N)]
u_alt = [pulp.LpVariable(f"u_alt_{i}", lowBound=0, cat='Continuous') for i in range(N)]
d = [pulp.LpVariable(f"d_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([price[i] * x[i] for i in range(N)])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= max_cpu

# Disk drive constraints
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk

# Memory constraints for 256K memory boards
problem += pulp.lpSum(u_256) >= min_memory
problem += pulp.lpSum(u_256) <= max_memory

# Alt memory constraint
problem += pulp.lpSum(u_alt) <= alt_memory

# Demand & preorder constraints
for i in range(N):
    problem += x[i] >= preorder[i]  # Fulfill preorder
    problem += x[i] <= demand[i]  # Demand constraint

# WS and GP demand constraints
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_GP
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_WS

# Memory allocation constraint per system
for i in range(N):
    problem += u_256[i] + u_alt[i] == memory_boards[i] * x[i]
    if not alt_compatible[i]:
        problem += u_alt[i] == 0

# Solve the problem
problem.solve()

# Collecting results
system_output = []
for i in range(N):
    num_produced = pulp.value(x[i])
    total_256K_boards_used = pulp.value(u_256[i])
    total_alt_boards_used = pulp.value(u_alt[i])
    total_disk_drives_used = pulp.value(x[i]) * disk_drives[i]
    system_output.append({
        "num_produced": num_produced,
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

# Calculate the total profit
profit = pulp.value(problem.objective)

# Output result
output = {
    "system_output": system_output,
    "profit": profit
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output