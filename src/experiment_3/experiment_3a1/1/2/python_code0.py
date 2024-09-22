import pulp
import json

# Data setup
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
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0, cat='Integer')

# Objective Function
c_disk = 50  # hypothetical cost per disk drive
c_mem = 100  # hypothetical cost per memory board
c_alt = 200  # hypothetical cost per alternative memory board

problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_disk * data['DiskDrives'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_mem * data['MemoryBoards'][i] * x[i] for i in range(data['N'])) - \
            pulp.lpSum(c_alt * y[i] for i in range(data['N']))

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Disk_Supply_Lower_Bound"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Supply_Upper_Bound"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Memory_Supply_Lower_Bound"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Supply_Upper_Bound"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General_Purpose_Demand"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += y[i] <= data['AltMemory'], f"Alternative_Memory_Usage_Limit_{i}"
        problem += y[i] <= data['MemoryBoards'][i] * x[i], f"Alternative_Memory_Usage_Only_If_Compatible_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "system_output": [
        {
            "Produced": x[i].varValue,
            "MemoryUsed": data['MemoryBoards'][i] * x[i].varValue,
            "AltMemoryUsed": y[i].varValue,
            "DiskUsed": data['DiskDrives'][i] * x[i].varValue
        } for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

# Output result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')