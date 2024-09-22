import json
import pulp

# Input data in JSON format
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

# Extract data from the input
N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_memory = data['MinMemory']
max_memory = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_memory = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
production_vars = [pulp.LpVariable(f'x{i}', lowBound=0) for i in range(N)]

# Objective function
problem += pulp.lpSum([price[i] * production_vars[i] for i in range(N)])

# Constraints
# Total CPU constraint
problem += pulp.lpSum(production_vars) <= max_cpu, "Max_CPU"

# Total demand constraints
for i in range(N):
    problem += production_vars[i] <= demand[i], f"Demand_{i}"

# Workstation and General purpose family constraints
problem += pulp.lpSum(production_vars[i] for i in range(N) if is_workstation[i]) <= demand_ws, "Max_Demand_WS"
problem += pulp.lpSum(production_vars[i] for i in range(N) if not is_workstation[i]) <= demand_gp, "Max_Demand_GP"

# Disk drives constraints
disk_used = pulp.lpSum(disk_drives[i] * production_vars[i] for i in range(N))
problem += disk_used >= min_disk, "Min_Disk"
problem += disk_used <= max_disk, "Max_Disk"

# Memory board constraints
mem_used = pulp.lpSum(memory_boards[i] * production_vars[i] for i in range(N))
problem += mem_used >= min_memory, "Min_Memory"
problem += mem_used <= max_memory, "Max_Memory"

# Alternative memory constraint
alt_used = pulp.lpSum(alt_memory if alt_compatible[i] else 0 for i in range(N))
problem += alt_used <= alt_memory, "Alt_Memory"

# Solving the problem
problem.solve()

# Preparing output
system_output = [
    {
        "num_produced": pulp.value(production_vars[i]),
        "total_256K_boards_used": pulp.value(memory_boards[i] * production_vars[i]),
        "total_alt_boards_used": pulp.value(alt_memory if alt_compatible[i] else 0),
        "total_disk_drives_used": pulp.value(disk_drives[i] * production_vars[i])
    }
    for i in range(N)
]

profit = pulp.value(problem.objective)

# Creating output JSON
output = {
    "system_output": system_output,
    "profit": profit
}

# Print the output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')