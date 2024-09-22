import pulp
import json

# Data from JSON format
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # number of systems produced
mem_used = pulp.LpVariable.dicts("mem_used", range(data['N']), lowBound=0)  # memory boards used
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0)  # alternative memory used
disk_used = pulp.LpVariable.dicts("disk_used", range(data['N']), lowBound=0)  # disk drives used

# Objective function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"

# Memory usage equations
for i in range(data['N']):
    problem += mem_used[i] + alt_used[i] == data['MemoryBoards'][i] * x[i], f"Memory_Usage_{i}"

# Alternative memory constraints
for i in range(data['N']):
    problem += alt_used[i] <= data['AltCompatible'][i] * data['AltMemory'], f"Alt_Mem_Usage_{i}"

# Demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

# General-purpose and workstation constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_Demand_Constraint"

# Preorder constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')