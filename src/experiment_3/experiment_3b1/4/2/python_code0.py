import pulp
import json

# Data from the provided JSON
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

# Problem definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
alt = [pulp.LpVariable(f'alt_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
# CPU Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

# Disk Drive Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# Memory Board Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(alt[i] for i in range(data['N'])) <= data['MaxMemory']

# Demand Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

# Alternative Memory Board Usage Constraints
for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += alt[i] <= data['AltMemory']

# Solve the problem
problem.solve()

# Print the results
result = {f'x[{i}]': x[i].varValue for i in range(data['N'])}
result['Objective'] = pulp.value(problem.objective)
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')