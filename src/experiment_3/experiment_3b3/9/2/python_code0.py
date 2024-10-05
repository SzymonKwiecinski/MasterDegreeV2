import pulp

# Data setup
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

# Problem
problem = pulp.LpProblem("DEC_Computer_Systems_Production", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective Function
revenue = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += revenue, "Total Revenue"

# Constraints

# Disk Drive Supply
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Drive_Supply"

# Memory Supply
problem += (pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) +
            pulp.lpSum(y[i] for i in range(data['N']))) <= data['MaxMemory'], "Memory_Supply"

# CPU Supply
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Supply"

# Demand for each system
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_System_{i}"

# Demand for GP family
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Family"

# Demand for WS family
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Family"

# Preorders must be fulfilled
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_System_{i}"

# Alternative Memory Constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += y[i] <= data['AltMemory'], f"Alternative_Memory_System_{i}"

# Solve the problem
problem.solve()

# Output results
system_output = [{"system_id": i, "units_produced": x[i].varValue, "alternative_memory_used": y[i].varValue} for i in range(data['N'])]
profit = pulp.value(problem.objective)
output = {
    "system_output": system_output,
    "profit": profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')