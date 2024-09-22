import pulp
import json

data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

# Model Initialization
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Continuous variable
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

# Disk Drive Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# 256K Memory Board Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] * data['AltCompatible'][i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt_used[i] * data['AltCompatible'][i] for i in range(data['N'])) <= data['MaxMemory']

# Demand Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']

# Alternative Memory Board Usage
for i in range(data['N']):
    problem += alt_used[i] <= data['AltMemory'] * data['AltCompatible'][i]

# Solve the problem
problem.solve()

# Output the results
system_output = {}
for i in range(data['N']):
    system_output[i] = {
        'num_produced': x[i].varValue,
        'total_256K_boards_used': data['MemoryBoards'][i] * x[i].varValue,
        'total_alt_boards_used': alt_used[i].varValue,
        'total_disk_drives_used': data['DiskDrives'][i] * x[i].varValue
    }

profit_value = pulp.value(problem.objective)

print(f'System Output: {system_output}')
print(f'Profit: {profit_value}')
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')