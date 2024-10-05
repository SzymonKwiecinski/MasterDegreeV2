import pulp

# Data
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
max_mem = data['MaxMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_mem = data['AltMemory']

# Define the problem
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision variables
x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(N)]
y_vars = [pulp.LpVariable(f"y_{i}", lowBound=0, cat='Integer') for i in range(N)]
z_vars = [pulp.LpVariable(f"z_{i}", lowBound=0, cat='Integer') for i in range(N)]
d_vars = [pulp.LpVariable(f"d_{i}", lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum([price[i] * x_vars[i] for i in range(N)]), "Total_Profit"

# Constraints
# CPU constraint
problem += pulp.lpSum([x_vars[i] for i in range(N)]) <= max_cpu, "CPU_Constraint"

# Disk drives constraints
problem += pulp.lpSum([disk_drives[i] * x_vars[i] for i in range(N)]) >= min_disk, "Min_Disk_Constraint"
problem += pulp.lpSum([disk_drives[i] * x_vars[i] for i in range(N)]) <= max_disk, "Max_Disk_Constraint"

# Memory constraints
problem += pulp.lpSum([memory_boards[i] * x_vars[i] + z_vars[i] for i in range(N)]) <= max_mem, "Max_Memory_Constraint"

for i in range(N):
    if alt_compatible[i]:
        problem += z_vars[i] <= alt_mem, f"Alt_Memory_Constraint_{i}"

# Demand constraints for systems
for i in range(N):
    problem += preorder[i] + x_vars[i] <= demand[i], f"Demand_Constraint_{i}"

# GP Family Demand Constraint
problem += pulp.lpSum([x_vars[i] for i in range(N) if not is_workstation[i]]) <= demand_GP, "GP_Family_Demand"

# WS Family Demand Constraint
problem += pulp.lpSum([x_vars[i] for i in range(N) if is_workstation[i]]) <= demand_WS, "WS_Family_Demand"

# Solve the problem
problem.solve()

# Output
system_output = [{
    "num_produced": pulp.value(x_vars[i]),
    "total_256K_boards_used": pulp.value(y_vars[i]),
    "total_alt_boards_used": pulp.value(z_vars[i]),
    "total_disk_drives_used": pulp.value(d_vars[i])
} for i in range(N)]

result = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')