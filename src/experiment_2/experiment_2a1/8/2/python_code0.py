import pulp
import json

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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of each system to produce
x = pulp.LpVariable.dicts("prod", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum([price[i] * x[i] for i in range(N)])

# Constraints
# CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu, "Max_CPU_Constraint"

# Disk drives constraint
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) >= min_disk, "Min_Disk_Constraint"
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk, "Max_Disk_Constraint"

# Memory constraints
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) >= min_mem, "Min_Memory_Constraint"
problem += pulp.lpSum([mem_boards[i] * x[i] for i in range(N)]) <= max_mem, "Max_Memory_Constraint"

# Demand constraints
for i in range(N):
    problem += x[i] <= demand[i], f"Demand_Constraint_{i}"

# Preorder constraints
for i in range(N):
    if preorder[i] > 0:
        problem += x[i] >= preorder[i], f"Preorder_Constraint_{i}"

# Workstation and General Purpose family constraints
problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws, "Max_WS_Demand_Constraint"
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp, "Max_GP_Demand_Constraint"

# Solve the problem
problem.solve()

# Collect the results
system_output = []
total_profit = pulp.value(problem.objective)

for i in range(N):
    if x[i].varValue > 0:
        system_output.append({
            "num_produced": x[i].varValue,
            "total_256K_boards_used": mem_boards[i] * x[i].varValue,
            "total_alt_boards_used": alt_mem if alt_compatible[i] else 0,
            "total_disk_drives_used": disk_drives[i] * x[i].varValue
        })

# Prepare final output
output = {
    "system_output": system_output,
    "profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

# Output the result as JSON
print(json.dumps(output, indent=4))