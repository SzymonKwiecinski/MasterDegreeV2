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
problem = pulp.LpProblem("Mixed_Integer_Programming_for_DEC", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(N)]
z = [pulp.LpVariable(f'z_{i}', lowBound=0, cat='Continuous') for i in range(N)]
d = [pulp.LpVariable(f'd_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(N))

# Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu'], "CPU_constraint"
problem += pulp.lpSum(d[i] for i in range(N)) >= data['MinDisk'], "Min_Disk_supply_constraint"
problem += pulp.lpSum(d[i] for i in range(N)) <= data['MaxDisk'], "Max_Disk_supply_constraint"
problem += pulp.lpSum(y[i] for i in range(N)) >= data['MinMemory'], "Min_256K_Memory_supply_constraint"
problem += pulp.lpSum(y[i] for i in range(N)) <= data['MaxMemory'], "Max_256K_Memory_supply_constraint"
problem += pulp.lpSum(z[i] for i in range(N)) <= data['AltMemory'], "Alternative_memory_constraint"

for i in range(N):
    problem += y[i] + z[i] >= data['MemoryBoards'][i] * x[i], f"Memory_requirement_system_{i}"
    problem += d[i] >= data['DiskDrives'][i] * x[i], f"Disk_requirement_system_{i}"
    problem += x[i] <= data['Demand'][i], f"Individual_system_demand_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_fulfillment_{i}"
    if not data['AltCompatible'][i]:
        problem += z[i] == 0, f"Alternative_memory_compatibility_{i}"

problem += pulp.lpSum(x[i] for i in GP_indices) <= data['DemandGP'], "GP_family_demand_constraint"
problem += pulp.lpSum(x[i] for i in WS_indices) <= data['DemandWS'], "WS_family_demand_constraint"

# Solve Problem
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')