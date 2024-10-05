import pulp
import json

# Load the data
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
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_mem = data['AltMemory']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
alt_used = [pulp.LpVariable(f'alt_used_{i}', lowBound=0, cat='Continuous') if alt_compatible[i] else 0 for i in range(N)]

# Objective function
profit = pulp.lpSum([price[i] * x[i] for i in range(N)])
problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(x) <= max_cpu, "CPU_Constraint"
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk, "Min_Disk_Constraint"
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk, "Max_Disk_Constraint"
problem += pulp.lpSum([memory_boards[i] * x[i] - alt_used[i] for i in range(N)]) >= min_mem, "Min_Mem_Constraint"
problem += pulp.lpSum([memory_boards[i] * x[i] - alt_used[i] for i in range(N)]) <= max_mem, "Max_Mem_Constraint"
problem += pulp.lpSum([alt_used[i] for i in range(N) if alt_compatible[i]]) <= alt_mem, "Alt_Mem_Constraint"

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i] + preorder[i], f"Demand_Constraint_{i}"
    if preorder[i] > 0:
        problem += x[i] >= preorder[i], f"Preorder_Constraint_{i}"

# Total demand for GP and WS systems
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp, "Total_GP_Demand"
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws, "Total_WS_Demand"

# Solve the problem
problem.solve()

# Prepare the output data
output_data = {
    "system_output": [
        {
            "num_produced": pulp.value(x[i]),
            "total_256K_boards_used": pulp.value(memory_boards[i] * x[i] - alt_used[i]) if alt_compatible[i] else pulp.value(memory_boards[i] * x[i]),
            "total_alt_boards_used": pulp.value(alt_used[i]) if alt_compatible[i] else 0,
            "total_disk_drives_used": pulp.value(disk_drives[i] * x[i])
        }
        for i in range(N)
    ],
    "profit": pulp.value(problem.objective)
}

# Print the result
print(json.dumps(output_data, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')