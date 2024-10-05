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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory"

# Demand Constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS"

# Pre-order Fulfillment
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

# Alternative Memory Usage Constraint
for i in range(data['N']):
    problem += alt_used[i] <= x[i] * data['AltCompatible'][i] * data['AltMemory'], f"Alt_Memory_Usage_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')