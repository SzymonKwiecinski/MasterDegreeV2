import pulp
import json

# Data from JSON format
data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

# Problem Setup
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
mem_used = pulp.LpVariable.dicts("mem_used", range(data['N']), lowBound=0, cat='Continuous')
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Continuous')
disk_used = pulp.LpVariable.dicts("disk_used", range(data['N']), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Drives_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] for i in range(data['N']) if data['AltCompatible'][i]) <= data['MaxMemory'] + data['AltMemory'], "Memory_Constraint"

# Demand Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General_Purpose_Demand"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand"
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Max_Demand_Constraint_{i}"

# Memory Usage Definitions
for i in range(data['N']):
    problem += mem_used[i] == data['MemoryBoards'][i] * x[i], f"Memory_Usage_{i}"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += alt_used[i] <= data['AltMemory'] * x[i], f"Alt_Memory_Usage_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')