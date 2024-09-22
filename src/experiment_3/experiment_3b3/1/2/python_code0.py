import pulp

# Data from json
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

# Sets and indices
N = data['N']
GP = [i for i in range(N) if not data['IsWorkstation'][i]]
WS = [i for i in range(N) if data['IsWorkstation'][i]]

# Decision variables
x = pulp.LpVariable.dicts('x', range(N), lowBound=0, cat='Continuous')
m = pulp.LpVariable.dicts('m', range(N), lowBound=0, cat='Continuous')
a = pulp.LpVariable.dicts('a', range(N), lowBound=0, cat='Continuous')
d = pulp.LpVariable.dicts('d', range(N), lowBound=0, cat='Continuous')

# Define the problem
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Objective function
profits = pulp.lpSum(data['Price'][i] * x[i] for i in range(N))
problem += profits, "Total Profit"

# Constraints

# CPU constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= data['MaxCpu'], "CPU Constraint"

# Disk drives constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) >= data['MinDisk'], "Min Disk Drives"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(N)) <= data['MaxDisk'], "Max Disk Drives"

# Memory constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] + a[i] for i in range(N)) <= data['MinMemory'], "Min Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] + a[i] for i in range(N)) <= data['MaxMemory'], "Max Memory"

# Demand and preorder constraints
for i in range(N):
    problem += x[i] >= data['Preorder'][i], f"Preorder Constraint {i}"

problem += pulp.lpSum(x[i] for i in GP) <= data['DemandGP'], "Demand GP"
problem += pulp.lpSum(x[i] for i in WS) <= data['DemandWS'], "Demand WS"

# Alternative memory board constraints
for i in range(N):
    problem += a[i] <= data['AltMemory'] * data['AltCompatible'][i], f"Alt Memory Constraint {i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')