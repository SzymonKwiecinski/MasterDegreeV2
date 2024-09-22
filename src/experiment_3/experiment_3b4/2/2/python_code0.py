import pulp

# Data from input
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

# Number of systems
N = data['N']

# Sets of systems
GP = [i for i, is_ws in enumerate(data['IsWorkstation']) if not is_ws]
WS = [i for i, is_ws in enumerate(data['IsWorkstation']) if is_ws]

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("z", range(N), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')

# Initialize the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Objective function
problem += pulp.lpSum([data['Price'][i] * x[i] for i in range(N)]), "Total_Profit"

# Constraints
# Disk constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(N)]) <= data['MaxDisk'], "Disk_Max"
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(N)]) >= data['MinDisk'], "Disk_Min"

# Memory constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(N)]) <= data['MaxMemory'], "Memory_Max"
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(N)]) >= data['MinMemory'], "Memory_Min"

# CPU constraint
problem += pulp.lpSum([x[i] for i in range(N)]) <= data['MaxCpu'], "CPU_Max"

# Demand constraints
for i in range(N):
    problem += x[i] <= data['Demand'][i], f"Demand_Individual_{i}"

# Group demand constraints
problem += pulp.lpSum([x[i] for i in GP]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum([x[i] for i in WS]) <= data['DemandWS'], "Demand_WS"

# Preorder constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i], f"Preorder_{i}"

# Alternative memory constraint
problem += pulp.lpSum([data['AltCompatible'][i] * y[i] for i in range(N)]) <= data['AltMemory'], "Alt_Memory"

# Memory type split constraints
for i in range(N):
    problem += x[i] == z[i] + y[i], f"Mem_Type_Split_{i}"

# Solve the problem
problem.solve()

# Print the total profit
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')