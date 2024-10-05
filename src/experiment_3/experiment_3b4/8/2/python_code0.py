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

# Problem
problem = pulp.LpProblem("DEC_Production_Planning", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data['Preorder'][i], cat='Continuous') for i in range(data['N'])]

# Objective
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints

# 1. CPU Constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu']

# 2. Disk Drive Supply Constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk']

# 3. Memory Boards Supply Constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory']

# 4. Demand Constraints for Each System
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]

# 5. Pre-order Fulfillment (Already addressed with lower bound in variable)

# 6. GP Systems Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']

# 7. WS Systems Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']

# 8. Alternative Memory Utilization
problem += pulp.lpSum((data['MemoryBoards'][i] * x[i] - data['MemoryBoards'][i]) for i in range(data['N']) if data['AltCompatible'][i]) <= data['AltMemory']

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')