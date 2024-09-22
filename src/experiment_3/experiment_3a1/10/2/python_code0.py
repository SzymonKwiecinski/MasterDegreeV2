import pulp
import json

# Data in JSON format
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

# Problem definition
problem = pulp.LpProblem("DEC_Production_Decision", pulp.LpMaximize)

# Variables
N = data['N']
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts("z", range(N), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(N))
problem += profit

# Constraints
# CPU Constraint
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu']

# Disk Drives Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) <= data['MaxDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) >= data['MinDisk']

# Memory Boards Constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(N)) <= data['MaxMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(N)) >= data['MinMemory']

# Demand Constraints
for i in range(N):
    problem += x[i] <= data['Demand'][i]

problem += pulp.lpSum(x[i] for i in range(N) if data['IsWorkstation'][i]) <= data['DemandWS']
problem += pulp.lpSum(x[i] for i in range(N) if not data['IsWorkstation'][i]) <= data['DemandGP']

# Preorder Constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i]

# Alternative Memory Boards Usage Constraint
for i in range(N):
    if data['AltCompatible'][i]:
        problem += z[i] <= data['AltMemory']

# 256K Boards Usage
for i in range(N):
    problem += y[i] == data['MemoryBoards'][i] * x[i]

# Disk Drives Usage
for i in range(N):
    problem += pulp.LpVariable(f'd_{i}', lowBound=0, cat='Integer') == data['DiskDrives'][i] * x[i]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')