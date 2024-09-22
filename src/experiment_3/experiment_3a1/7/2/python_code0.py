import pulp
import json

# Data from JSON
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

# Problem Definition
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Number of systems produced
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')  # Number of alternative memory boards used

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - pulp.lpSum(y[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"

for i in range(data['N']):
    problem += y[i] <= data['AltMemory'] * int(data['AltCompatible'][i]), f"Alt_Memory_Constraint_{i}"

# Solve the problem
problem.solve()

# Output
system_output = [
    {
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": pulp.value(pulp.lpSum(data['MemoryBoards'][j] * x[j] for j in range(data['N']))),
        "total_alt_boards_used": pulp.value(y[i]),
        "total_disk_drives_used": pulp.value(pulp.lpSum(data['DiskDrives'][j] * x[j] for j in range(data['N'])))
    } for i in range(data['N'])
]

profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

print(output)
print(f' (Objective Value): <OBJ>{profit}</OBJ>')