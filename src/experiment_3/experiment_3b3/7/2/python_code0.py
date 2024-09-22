import pulp

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

# Cost parameters
disk_cost = 100  # assumed cost of disk
board_cost = 200  # assumed cost of 256K memory board
alt_cost = 150  # assumed cost of alternative memory board

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
alt = [pulp.LpVariable(f'alt_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum([
    data['Price'][i] * x[i] - (data['MemoryBoards'][i] * board_cost + data['DiskDrives'][i] * disk_cost + alt[i] * alt_cost)
    for i in range(data['N'])
])

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk supply constraints
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) >= data['MinDisk']
problem += pulp.lpSum([data['DiskDrives'][i] * x[i] for i in range(data['N'])]) <= data['MaxDisk']

# Memory supply constraints
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) >= data['MinMemory']
problem += pulp.lpSum([data['MemoryBoards'][i] * x[i] for i in range(data['N'])]) <= data['MaxMemory']

# Demand constraints for each system
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i]
    problem += x[i] >= data['Preorder'][i]

# Total WS and GP demand constraints
problem += pulp.lpSum([x[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']
problem += pulp.lpSum([x[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']

# Alternative memory board constraints
for i in range(data['N']):
    problem += alt[i] <= data['AltMemory']
    problem += alt[i] <= data['AltCompatible'][i] * x[i]

# Solve the problem
problem.solve()

# Output
system_output = [{
    "num_produced": int(pulp.value(x[i])),
    "total_256K_boards_used": int(data['MemoryBoards'][i] * pulp.value(x[i])),
    "total_alt_boards_used": int(pulp.value(alt[i])),
    "total_disk_drives_used": int(data['DiskDrives'][i] * pulp.value(x[i]))
} for i in range(data['N'])]

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')