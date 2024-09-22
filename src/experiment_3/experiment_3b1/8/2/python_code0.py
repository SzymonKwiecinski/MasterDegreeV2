import pulp
import json

# Data input
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
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Boards_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"

for i in range(data['N']):
    problem += y[i] <= data['AltMemory'] * data['AltCompatible'][i], f"Alt_Memory_Usage_Constraint_{i}"

# Solve the problem
problem.solve()

# Output
output = {
    "system_output": [
        {
            "num_produced": x[i].varValue,
            "total_256K_boards_used": data['MemoryBoards'][i] * x[i].varValue,
            "total_alt_boards_used": y[i].varValue,
            "total_disk_drives_used": data['DiskDrives'][i] * x[i].varValue
        }
        for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')