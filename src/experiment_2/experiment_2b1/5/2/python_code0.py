import pulp
import json

# Input data from JSON
data = {'N': 5, 
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
        'AltMemory': 4000}

# Variables
N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
memory_boards = data['MemoryBoards']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand = data['Demand']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
num_produced = [pulp.LpVariable(f'num_produced_{i}', lowBound=0) for i in range(N)]
alt_boards_used = [pulp.LpVariable(f'alt_boards_used_{i}', lowBound=0) for i in range(N)]

# Objective Function
profit = pulp.lpSum([price[i] * num_produced[i] for i in range(N)])
problem += profit

# Constraints
problem += pulp.lpSum(num_produced[i] for i in range(N)) <= max_cpu  # CPU constraint

# Disk capacity constraints
problem += pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N)) >= min_disk
problem += pulp.lpSum(disk_drives[i] * num_produced[i] for i in range(N)) <= max_disk

# Memory capacity constraints
problem += pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N)) + \
           pulp.lpSum(alt_boards_used[i] for i in range(N)) >= min_mem
problem += pulp.lpSum(memory_boards[i] * num_produced[i] for i in range(N)) + \
           pulp.lpSum(alt_boards_used[i] for i in range(N)) <= max_mem

# Demand constraints
for i in range(N):
    problem += num_produced[i] <= demand[i] - preorder[i]

# Workstation and General-Purpose demands
problem += pulp.lpSum(num_produced[i] for i in range(N) if is_workstation[i]) <= demand_ws
problem += pulp.lpSum(num_produced[i] for i in range(N) if not is_workstation[i]) <= demand_gp

# Alternative memory constraints
for i in range(N):
    if alt_compatible[i]:
        problem += alt_boards_used[i] <= alt_mem

# Solve the problem
problem.solve()

# Collect results
system_output = []
for i in range(N):
    if pulp.value(num_produced[i]) > 0:
        system_output.append({
            "num_produced": pulp.value(num_produced[i]),
            "total_256K_boards_used": pulp.value(memory_boards[i] * num_produced[i]),
            "total_alt_boards_used": pulp.value(alt_boards_used[i]),
            "total_disk_drives_used": pulp.value(disk_drives[i] * num_produced[i])
        })

# Construct final output
result = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result in JSON format
output_json = json.dumps(result)
print(output_json)