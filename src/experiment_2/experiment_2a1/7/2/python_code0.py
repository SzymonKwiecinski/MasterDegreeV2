import pulp
import json

data = {'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}

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
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
alt_memory = data['AltMemory']
alt_compatible = data['AltCompatible']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x{i}', lowBound=0) for i in range(N)]  # number of systems produced

# Objective function: Maximize profit
profit = pulp.lpSum(price[i] * x[i] for i in range(N))
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(x) <= max_cpu

# Disk drive constraints
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) >= min_disk
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) <= max_disk

# Memory constraints
problem += pulp.lpSum(memory_boards[i] * x[i] for i in range(N) if not alt_compatible[i]) >= min_memory
problem += pulp.lpSum(memory_boards[i] * x[i] for i in range(N) if not alt_compatible[i]) <= max_memory
problem += pulp.lpSum(x[i] for i in range(N) if alt_compatible[i]) <= alt_memory

# Demand constraints including preorders
for i in range(N):
    problem += x[i] >= preorder[i]  # fulfill preorders
    problem += x[i] <= demand[i]  # not exceeding demand

# GP and WS demand constraints
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_GP
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_WS

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(N):
    system_output.append({
        "num_produced": x[i].value(),
        "total_256K_boards_used": memory_boards[i] * x[i].value(),
        "total_alt_boards_used": alt_compatible[i] * x[i].value(),
        "total_disk_drives_used": disk_drives[i] * x[i].value()
    })

profit_value = pulp.value(problem.objective)

# Output result
result = {
    "system_output": system_output,
    "profit": profit_value
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')