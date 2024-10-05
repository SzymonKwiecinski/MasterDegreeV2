import json
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

# Model
problem = pulp.LpProblem("DEC_Production_Planning", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts('x', range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts('y', range(data['N']), lowBound=0, cat='Integer')
z = pulp.LpVariable.dicts('z', range(data['N']), lowBound=0, cat='Integer')
w = pulp.LpVariable.dicts('w', range(data['N']), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"
problem += pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"
problem += pulp.lpSum(z[i] for i in range(data['N'])) <= data['AltMemory'], "Max_Alt_Memory"
problem += pulp.lpSum(w[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(w[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_{i}"
    problem += (pulp.lpSum(x[j] for j in range(data['N']) if not data['IsWorkstation'][j]) 
                <= data['DemandGP']), f"Demand_GP_{i}"
    problem += (pulp.lpSum(x[j] for j in range(data['N']) if data['IsWorkstation'][j]) 
                <= data['DemandWS']), f"Demand_WS_{i}"
    problem += x[i] <= data['Demand'][i], f"Demand_{i}"
    if not data['AltCompatible'][i]:
        problem += z[i] == 0, f"No_Alt_Memory_{i}"
    problem += y[i] + z[i] == data['MemoryBoards'][i] * x[i], f"Memory_Board_Constraint_{i}"
    problem += w[i] == data['DiskDrives'][i] * x[i], f"Disk_Drive_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')