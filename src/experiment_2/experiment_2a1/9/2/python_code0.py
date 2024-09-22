import json
import pulp

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
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand = data['Demand']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

# Create the LP problem
problem = pulp.LpProblem('DEC_Production_Problem', pulp.LpMaximize)

# Decision variables
num_produced = pulp.LpVariable.dicts("num_produced", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([(num_produced[i] * price[i]) for i in range(N)])
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(num_produced[i] for i in range(N)) <= max_cpu, "Max_CPU"

# Disk Drive Constraints
problem += pulp.lpSum(num_produced[i] * disk_drives[i] for i in range(N)) >= min_disk, "Min_Disk"
problem += pulp.lpSum(num_produced[i] * disk_drives[i] for i in range(N)) <= max_disk, "Max_Disk"

# Memory Board Constraints
problem += pulp.lpSum(num_produced[i] * memory_boards[i] for i in range(N)) >= min_mem, "Min_Memory"
problem += pulp.lpSum(num_produced[i] * memory_boards[i] for i in range(N)) <= max_mem, "Max_Memory"

# Demand Constraints for each system
for i in range(N):
    problem += num_produced[i] <= demand[i], f"Demand_Constraint_{i}"

# Demand Constraints for GP and WS families
problem += pulp.lpSum(num_produced[i] for i in range(N) if not is_workstation[i]) <= demand_GP, "Demand_GP_Constraint"
problem += pulp.lpSum(num_produced[i] for i in range(N) if is_workstation[i]) <= demand_WS, "Demand_WS_Constraint"

# Preorder Constraints
for i in range(N):
    problem += num_produced[i] >= preorder[i], f"Preorder_Constraint_{i}"

# Alternative Memory Board usage
total_mem_used = pulp.lpSum(num_produced[i] * memory_boards[i] for i in range(N))
problem += total_mem_used <= max_mem + alt_mem, "Alternative_Memory_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
system_output = []
profit_value = pulp.value(problem.objective)
for i in range(N):
    system_output.append({
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(num_produced[i] * memory_boards[i]),
        "total_alt_boards_used": pulp.value(num_produced[i] * (1 if alt_compatible[i] else 0)),  # Use alternative boards if compatible
        "total_disk_drives_used": pulp.value(num_produced[i] * disk_drives[i])
    })

output_result = {
    "system_output": system_output,
    "profit": profit_value
}

# Print output in the required format
print(json.dumps(output_result))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')