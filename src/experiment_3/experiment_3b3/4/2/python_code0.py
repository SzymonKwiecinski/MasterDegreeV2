import pulp

# Data
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

# Variables
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
min_memory = data['MinMemory']
max_memory = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']
alt_memory = data['AltMemory']

# Create a Linear Programming Problem
problem = pulp.LpProblem("DEC_Computer_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
cost_of_boards = [memory_boards[i] * x[i] + alt_memory * y[i] for i in range(N)]
cost_of_disks = [disk_drives[i] * x[i] for i in range(N)]
profit = pulp.lpSum([price[i] * x[i] - cost_of_boards[i] - cost_of_disks[i] for i in range(N)])
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(x) <= max_cpu

# Disk Drive Constraint
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk

# Memory Board Constraint
problem += pulp.lpSum([memory_boards[i] * x[i] for i in range(N)]) + pulp.lpSum([y[i] * alt_compatible[i] for i in range(N)]) <= max_memory

# Preorder Fulfillment and Individual Demand
for i in range(N):
    problem += x[i] >= preorder[i]
    problem += x[i] <= demand[i]

# GP and WS Family Demand
for i in range(N):
    if not is_workstation[i]:
        problem += x[i] <= demand_gp
    else:
        problem += x[i] <= demand_ws

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')