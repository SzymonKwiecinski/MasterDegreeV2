import pulp
import json

# Data provided in JSON format
data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

# Initialize the problem
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
problem += profit, "Total_Profit"

# Constraints
# 1. CPU constraint
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"

# 2. Disk drives constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"

# 3. Memory boards constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + 
           pulp.lpSum(x[i] if data['AltCompatible'][i] else 0 for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) + 
           pulp.lpSum(x[i] if data['AltCompatible'][i] else 0 for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"

# 4. Demand constraints for each system
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

# 5. Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS_Constraint"

# 6. Preorder constraints
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

# Solve the problem
problem.solve()

# Output results
produced = {i: x[i].varValue for i in range(data['N'])}
total_memory_used = sum(data['MemoryBoards'][i] * produced[i] for i in range(data['N']))
total_alt_used = sum(produced[i] if data['AltCompatible'][i] else 0 for i in range(data['N']))
total_disk_used = sum(data['DiskDrives'][i] * produced[i] for i in range(data['N']))

print(f'Produced Systems: {produced}')
print(f'Total Memory Boards Used: {total_memory_used}')
print(f'Total Alternative Boards Used: {total_alt_used}')
print(f'Total Disk Drives Used: {total_disk_used}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')