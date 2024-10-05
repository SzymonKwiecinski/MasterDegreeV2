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

# Indices
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

# Problem
problem = pulp.LpProblem("DEC_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat=pulp.LpContinuous)
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat=pulp.LpInteger)

# Objective function
problem += pulp.lpSum([price[i] * x[i] for i in range(N)])

# Constraints
problem += pulp.lpSum([x[i] for i in range(N)]) <= max_cpu
problem += pulp.lpSum([disk_drives[i] * x[i] for i in range(N)]) <= max_disk
problem += pulp.lpSum([memory_boards[i] * x[i] + y[i] for i in range(N)]) <= max_memory
problem += pulp.lpSum([x[i] for i in range(N)]) >= pulp.lpSum([preorder[i] for i in range(N)])

for i in range(N):
    problem += x[i] <= demand[i]
    problem += x[i] >= preorder[i]
    if alt_compatible[i]:
        problem += y[i] <= alt_memory

problem += pulp.lpSum([x[i] for i in range(N) if is_workstation[i]]) <= demand_ws
problem += pulp.lpSum([x[i] for i in range(N) if not is_workstation[i]]) <= demand_gp

# Solve
problem.solve()

# Output
system_output = [(i, x[i].varValue, y[i].varValue) for i in range(N)]
profit = pulp.value(problem.objective)

print("System Output:", system_output)
print(f"Profit (Objective Value): <OBJ>{profit}</OBJ>")