import pulp
import json

# Given data in JSON format
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
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Number of systems produced
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0)  # Alternative memory boards used

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) 
cost_of_components = 0  # Assuming it is defined somewhere or zero for simplicity
problem += profit - cost_of_components

# Resource Constraints
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Drives_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Constraint"
problem += pulp.lpSum(y[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative_Memory_Usage"

# Production Constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"
    
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"System_Demand_Constraint_{i}"

# Solve the problem
problem.solve()

# Output result
system_output = {i: x[i].varValue for i in range(data['N'])}
total_profit = pulp.value(problem.objective)

print(f'Systems Produced: {system_output}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')