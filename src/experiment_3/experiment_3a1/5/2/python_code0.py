import pulp
import json

# Data provided in JSON format
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
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['Demand'][i]) for i in range(data['N'])]
alt_used = [pulp.LpVariable(f'alt_used_{i}', lowBound=0) for i in range(data['N']) if data['AltCompatible'][i]]

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))  # Total revenue
costs = 0  # Assuming no costs are defined in the input, modify if needed
problem += profit - costs, "Total_Profit"

# Constraints
# CPU Constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"

# Disk Drives Constraint
problem += (pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint")
problem += (pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint")

# Memory Boards Constraint
problem += (pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + 
            pulp.lpSum(alt_used[i] for i in range(data['N']) if data['AltCompatible'][i]) >= data['MinMemory'], "Min_Memory_Constraint")
problem += (pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + 
            pulp.lpSum(alt_used[i] for i in range(data['N']) if data['AltCompatible'][i]) <= data['MaxMemory'], "Max_Memory_Constraint")

# Preorder Fulfillment
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_{i}"

# Workstation and General Purpose Demand Constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General_Purpose_Demand_Constraint"

# Individual System Demand Constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Individual_Demand_Constraint_{i}"

# Solve the problem
problem.solve()

# Output results
system_output = {f'system_{i}': {'produced': pulp.value(x[i]), 'alt_used': pulp.value(alt_used[i]) if data['AltCompatible'][i] else 0} for i in range(data['N'])}
profit_value = pulp.value(problem.objective)

output = {
    'system_output': system_output,
    'profit': profit_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')