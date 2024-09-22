import pulp
import json

# Load data
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

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(data['N'])]  # Systems produced
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0) for i in range(data['N'])]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0) for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0) for i in range(data['N'])]

# Objective function: Maximize profit
profit = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
problem += profit

# Constraints

# CPU constraint
problem += pulp.lpSum(x) <= data['MaxCpu']

# Disk drive constraints
problem += pulp.lpSum(disk_used[i] for i in range(data['N'])) >= data['MinDisk']
problem += pulp.lpSum(disk_used[i] for i in range(data['N'])) <= data['MaxDisk']

# Memory board constraints
problem += pulp.lpSum(mem_used[i] + alt_used[i] for i in range(data['N'])) >= data['MinMemory']
problem += pulp.lpSum(mem_used[i] + alt_used[i] for i in range(data['N'])) <= data['MaxMemory']

# Demand and preorder constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i]
    problem += x[i] <= data['Demand'][i]

# GP and WS demand constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP']
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS']

# Disk drive usage
for i in range(data['N']):
    problem += disk_used[i] == data['DiskDrives'][i] * x[i]

# Memory board usage
for i in range(data['N']):
    problem += mem_used[i] + alt_used[i] == data['MemoryBoards'][i] * x[i]
    if not data['AltCompatible'][i]:
        problem += alt_used[i] == 0

# Alternative memory board constraint
problem += pulp.lpSum(alt_used[i] for i in range(data['N'])) <= data['AltMemory']

# Solve the problem
problem.solve()

# Prepare output
output_data = {
    "system_output": [
        {
            "num_produced": x[i].varValue,
            "total_256K_boards_used": mem_used[i].varValue,
            "total_alt_boards_used": alt_used[i].varValue,
            "total_disk_drives_used": disk_used[i].varValue
        }
        for i in range(data['N'])
    ],
    "profit": pulp.value(problem.objective)
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the result as JSON
print(json.dumps(output_data, indent=4))