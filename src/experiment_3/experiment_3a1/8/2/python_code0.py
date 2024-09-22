import pulp

# Data from the given JSON
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

# Create the optimization problem
problem = pulp.LpProblem("Computer_Systems_Production", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(data['Price'][i-1] * x[i] for i in range(1, data['N'] + 1))
costs = pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1))  # Assuming cost is related to memory boards
problem += profit - costs, "Total_Profit"

# Constraints
# CPU constraint
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu'], "CPU_Constraint"

# Disk drive constraints
problem += pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i-1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk'], "Max_Disk_Constraint"

# Memory board constraints
problem += pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinMemory'], "Min_Memory_Constraint"
problem += (pulp.lpSum(data['MemoryBoards'][i-1] * x[i] for i in range(1, data['N'] + 1)) + 
             pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['AltCompatible'][i-1])) <= data['MaxMemory'] + data['AltMemory'], "Max_Memory_Constraint"

# Demand constraints for workstations and general-purpose
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i-1]) <= data['DemandWS'], "Demand_WS_Constraint"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i-1]) <= data['DemandGP'], "Demand_GP_Constraint"

# Preorder constraints
for i in range(1, data['N'] + 1):
    problem += x[i] >= data['Preorder'][i-1], f"Preorder_Constraint_{i}"

# Demand limits
for i in range(1, data['N'] + 1):
    problem += x[i] <= data['Demand'][i-1], f"Demand_Limit_{i}"

# Solve the problem
problem.solve()

# Prepare output
system_output = []
for i in range(1, data['N'] + 1):
    boards_used = data['MemoryBoards'][i-1] * x[i].varValue
    alt_boards_used = x[i].varValue if data['AltCompatible'][i-1] else 0
    disk_used = data['DiskDrives'][i-1] * x[i].varValue
    system_output.append({
        "num_produced": x[i].varValue,
        "total_256K_boards_used": boards_used,
        "total_alt_boards_used": alt_boards_used,
        "total_disk_drives_used": disk_used
    })

total_profit = pulp.value(problem.objective)

# Output the result
import json
result = {
    "system_output": system_output,
    "profit": total_profit
}
print(json.dumps(result, indent=4))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')