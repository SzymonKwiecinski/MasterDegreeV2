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
GP_indices = [i for i in range(N) if not data['IsWorkstation'][i]]
WS_indices = [i for i in range(N) if data['IsWorkstation'][i]]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0) for i in range(N)]
z = [pulp.LpVariable(f'z_{i}', lowBound=0) for i in range(N)]
d = [pulp.LpVariable(f'd_{i}', lowBound=0) for i in range(N)]

# Objective Function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(N)])
problem += profit

# Constraints
problem += pulp.lpSum(x) <= data['MaxCpu'], "CPU Supply Constraint"
problem += pulp.lpSum(d) >= data['MinDisk'], "Min Disk Supply Constraint"
problem += pulp.lpSum(d) <= data['MaxDisk'], "Max Disk Supply Constraint"
problem += pulp.lpSum(y) >= data['MinMemory'], "Min Memory Constraint"
problem += pulp.lpSum(y) <= data['MaxMemory'], "Max Memory Constraint"
problem += pulp.lpSum([x[i] for i in GP_indices]) <= data['DemandGP'], "GP Demand"
problem += pulp.lpSum([x[i] for i in WS_indices]) <= data['DemandWS'], "WS Demand"

for i in range(N):
    problem += x[i] <= data['Demand'][i], f"System Demand Constraint {i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder Fulfillment {i}"
    problem += y[i] == data['MemoryBoards'][i] * x[i], f"Memory Usage {i}"
    problem += d[i] == data['DiskDrives'][i] * x[i], f"Disk Usage {i}"
    if data['AltCompatible'][i]:
        problem += z[i] <= data['AltMemory'], f"Alternative Memory Supply {i}"
    else:
        problem += z[i] == 0, f"Alternative Memory Usage Constraint {i}"

# Solve
problem.solve()

# Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')