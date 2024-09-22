import pulp
import json

# Data from provided JSON
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
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_memory = data['AltMemory']
demand_GP = data['DemandGP']
demand_WS = data['DemandWS']
max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
alt_compatible = data['AltCompatible']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  # number of systems produced (continuous)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  # number of alternative memory boards used (integer)

# Objective Function
profit_expression = pulp.lpSum(price[i] * x[i] for i in range(N)) - pulp.lpSum(y[i] for i in range(N))
problem += profit_expression

# Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu, "CPU_constraint"
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) >= min_disk, "Min_disk_drives"
problem += pulp.lpSum(disk_drives[i] * x[i] for i in range(N)) <= max_disk, "Max_disk_drives"
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) + pulp.lpSum(y[i] for i in range(N)) >= min_mem, "Min_memory_boards"
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) + pulp.lpSum(y[i] for i in range(N)) <= max_mem, "Max_memory_boards"
for i in range(N):
    problem += x[i] >= preorder[i], f"Preorder_constraint_{i}"
    problem += x[i] <= demand[i], f"Demand_constraint_{i}"
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_WS, "Workstation_demand"
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_GP, "General_purpose_demand"
for i in range(N):
    problem += y[i] <= alt_memory * alt_compatible[i], f"Alt_memory_constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
system_output = [{"system_id": i, "produced": pulp.value(x[i]), "alt_memory_used": pulp.value(y[i])} for i in range(N)]
profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{profit}</OBJ>')