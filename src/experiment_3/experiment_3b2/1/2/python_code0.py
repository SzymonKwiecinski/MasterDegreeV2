import pulp
import json

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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("System", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
disk_used = pulp.LpVariable.dicts("DiskUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
mem_used = pulp.LpVariable.dicts("MemUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')
alt_used = pulp.LpVariable.dicts("AltUsed", range(1, data['N'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Price'][i-1] * x[i] for i in range(1, data['N'] + 1)), "Total_Profit"

# Constraints
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu']), "CPU_Constraint"
problem += (data['MinDisk'] <= pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk']), "Disk_Constraint"
problem += (data['MinMemory'] <= pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxMemory']), "Memory_Constraint"

# Demand constraints for each system
for i in range(1, data['N'] + 1):
    problem += (x[i] <= data['Demand'][i-1]), f"Demand_Constraint_{i}"

# GP and WS demand constraints
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i-1]) <= data['DemandGP']), "GP_Demand_Constraint"
problem += (pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i-1]) <= data['DemandWS']), "WS_Demand_Constraint"

# Preorder fulfillment constraints
for i in range(1, data['N'] + 1):
    problem += (x[i] >= data['Preorder'][i-1]), f"Preorder_Constraint_{i}"

# Memory usage equations
for i in range(1, data['N'] + 1):
    problem += (mem_used[i] == data['MemoryBoards'][i-1] * x[i]), f"Memory_Usage_{i}"

# Incompatible alternative memory use
for i in range(1, data['N'] + 1):
    if not data['AltCompatible'][i-1]:
        problem += (alt_used[i] == 0), f"Alt_Memory_Incompatible_{i}"

# Alternative memory supply constraint
problem += (pulp.lpSum(alt_used[i] for i in range(1, data['N'] + 1)) <= data['AltMemory']), "Alt_Memory_Supply_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')