import pulp
import json

data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

# Create the linear programming problem
problem = pulp.LpProblem("DEC_Production_Planning", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "Demand_GP"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Demand_WS"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

for i in range(data['N']):
    if data['AltCompatible'][i]:
        problem += x[i] <= data['AltMemory'], f"Alt_Memory_Constraint_{i}"

for i in range(data['N']):
    problem += x[i] == data['MemoryBoards'][i] * x[i], f"Memory_Used_{i}"

for i in range(data['N']):
    problem += x[i] == data['DiskDrives'][i] * x[i], f"Disk_Used_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')