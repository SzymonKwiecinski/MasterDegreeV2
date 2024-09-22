import pulp
import json

data = {'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 
        'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 
        'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 
        'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 
        'DemandWS': 3200, 'AltMemory': 4000}

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk_drives = data['DiskDrives']
mem_boards = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Produce", range(N), lowBound=0, cat='Continuous')

# Objective function: maximize profit
problem += pulp.lpSum([price[i] * x[i] for i in range(N)])

# Constraints
# CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu

# Disk drives constraint
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk

# Memory constraints
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) >= min_mem
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) <= max_mem

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i]

# Demand for GP and WS
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i] == False]) <= demand_GP
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i] == True]) <= demand_WS

# Preorder constraints
for i in range(N):
    problem += x[i] >= preorder[i]

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(N):
    total_256K_boards_used = mem_boards[i] * x[i].varValue
    total_disk_drives_used = disk_drives[i] * x[i].varValue
    total_alt_boards_used = 0
    if alt_compatible[i]:
        total_alt_boards_used = min(alt_mem, alt_mem - (total_256K_boards_used - (max_mem - min_mem)))
    
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

output_json = json.dumps(output)
print(output_json)
print(f' (Objective Value): <OBJ>{profit}</OBJ>')