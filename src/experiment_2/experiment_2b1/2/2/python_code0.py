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
    'AltMemory': 4000
}

# Problem setup
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_systems = [pulp.LpVariable(f'num_system_{i}', lowBound=0) for i in range(N)]
total_memory_used = [pulp.LpVariable(f'total_mem_used_{i}', lowBound=0) for i in range(N)]
total_alt_memory_used = [pulp.LpVariable(f'total_alt_mem_used_{i}', lowBound=0) for i in range(N)]
total_disk_drives_used = [pulp.LpVariable(f'total_disk_used_{i}', lowBound=0) for i in range(N)]

# Objective function
profit = pulp.lpSum(price[i] * num_systems[i] for i in range(N))
problem += profit

# Constraints
problem += pulp.lpSum(num_systems[i] for i in range(N)) <= max_cpu  # CPU constraint

# Disk constraints
disk_used = pulp.lpSum(disk_drives[i] * num_systems[i] for i in range(N))
problem += disk_used >= min_disk
problem += disk_used <= max_disk

# Memory constraints
memory_used = pulp.lpSum(memory_boards[i] * num_systems[i] for i in range(N))
problem += memory_used >= min_memory
problem += memory_used <= max_memory

# Demand constraints
for i in range(N):
    problem += num_systems[i] <= demand[i]

# GP and WS demand constraints
problem += pulp.lpSum(num_systems[i] for i in range(N) if not is_workstation[i]) <= demand_gp
problem += pulp.lpSum(num_systems[i] for i in range(N) if is_workstation[i]) <= demand_ws

# Preorder constraints
for i in range(N):
    problem += num_systems[i] >= preorder[i]

# Solve the problem
problem.solve()

# Prepare the output
system_output = []
for i in range(N):
    system_output.append({
        "num_produced": pulp.value(num_systems[i]),
        "total_256K_boards_used": pulp.value(memory_boards[i] * num_systems[i]),
        "total_alt_boards_used": pulp.value(alt_memory * num_systems[i] if alt_compatible[i] else 0),
        "total_disk_drives_used": pulp.value(disk_drives[i] * num_systems[i])
    })

profit_value = pulp.value(problem.objective)

# Format output as requested
output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print the objective value
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')

# Output in JSON format
print(json.dumps(output, indent=4))