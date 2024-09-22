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
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

# Define the problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision variables: number of each system to produce
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum(price[i] * x[i] for i in range(N))
problem += profit

# Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu  # CPU constraint
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) >= min_disk  # Minimum disk constraint
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) <= max_disk  # Maximum disk constraint
problem += pulp.lpSum(mem_boards[i] * x[i] for i in range(N)) >= min_mem  # Minimum memory constraint
problem += pulp.lpSum(mem_boards[i] * x[i] for i in range(N)) <= max_mem  # Maximum memory constraint

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i]  # Individual system demand
    problem += x[i] >= preorder[i]  # Preorder constraints

# Family demand constraints
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_gp  # GP systems
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_ws  # WS systems

# Alternative memory constraint
total_mem_used = pulp.lpSum(mem_boards[i] * x[i] for i in range(N) if alt_compatible[i]) 
problem += total_mem_used <= alt_mem  # Usage of alternative memory boards

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(N):
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": mem_boards[i] * x[i].varValue,
        "total_alt_boards_used": alt_mem if alt_compatible[i] else 0,
        "total_disk_drives_used": disk_drives[i] * x[i].varValue
    })

profit_value = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit_value
}

# Print output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')