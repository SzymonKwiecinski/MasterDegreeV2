import pulp
import json

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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(N)]  # Number of systems produced

# Objective function
profit = pulp.lpSum(price[i] * x[i] for i in range(N))
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= max_cpu

# Disk drives constraint
total_disk = pulp.lpSum(disk_drives[i] * x[i] for i in range(N))
problem += total_disk >= min_disk
problem += total_disk <= max_disk

# Memory boards constraints
total_mem = pulp.lpSum(mem_boards[i] * x[i] for i in range(N))
problem += total_mem >= min_mem
problem += total_mem <= max_mem

# Demand constraints for each system
for i in range(N):
    problem += x[i] <= demand[i]

# Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_GP
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_WS

# Preorder constraints
for i in range(N):
    problem += x[i] >= preorder[i]

# Alternative memory constraint
if alt_mem > 0:
    total_alt_mem = pulp.lpSum(alt_mem if alt_compatible[i] else 0 for i in range(N))
    problem += total_mem + total_alt_mem <= max_mem

# Solve the problem
problem.solve()

# Prepare the output
system_output = []
for i in range(N):
    if x[i].varValue > 0:
        system_output.append({
            "num_produced": x[i].varValue,
            "total_256K_boards_used": mem_boards[i] * x[i].varValue,
            "total_alt_boards_used": (alt_mem if alt_compatible[i] else 0) * x[i].varValue,
            "total_disk_drives_used": disk_drives[i] * x[i].varValue
        })

profit_value = pulp.value(problem.objective)

# Output the results
output = {
    "system_output": system_output,
    "profit": profit_value
}

print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')
print(json.dumps(output, indent=4))