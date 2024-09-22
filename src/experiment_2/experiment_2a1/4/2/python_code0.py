import pulp
import json

# Input data
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

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]

# Objective function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
# CPU limit constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"

# Disk drives constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"

# Memory constraints
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"

# Demand constraints including preorders
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_{i}"
    
# Workstation and General-purpose family constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP"

# Solve the problem
problem.solve()

# Prepare output data
system_output = []
for i in range(data['N']):
    total_disk_drives_used = data['DiskDrives'][i] * pulp.value(x[i])
    total_256K_boards_used = data['MemoryBoards'][i] * pulp.value(x[i])
    total_alt_boards_used = (pulp.value(x[i]) * data['AltCompatible'][i] * min(data['AltMemory'], total_256K_boards_used)) if data['AltCompatible'][i] else 0

    system_output.append({
        "num_produced": pulp.value(x[i]),
        "total_256K_boards_used": total_256K_boards_used,
        "total_alt_boards_used": total_alt_boards_used,
        "total_disk_drives_used": total_disk_drives_used
    })

# Final output format
output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

# Print profit objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')