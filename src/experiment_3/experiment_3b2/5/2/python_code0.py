import pulp
import json

# Input data
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0)  # Number of systems to produce

# Objective Function
problem += pulp.lpSum(data['Price'][i - 1] * x[i] for i in range(1, data['N'] + 1)), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1)) <= data['MaxCpu'], "CPU_Availability"
problem += pulp.lpSum(data['DiskDrives'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxDisk'], "Disk_Upper_Limit"
problem += pulp.lpSum(data['DiskDrives'][i - 1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinDisk'], "Disk_Lower_Limit"
problem += pulp.lpSum(data['MemoryBoards'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxMemory'], "Memory_Upper_Limit"
problem += pulp.lpSum(data['MemoryBoards'][i - 1] * x[i] for i in range(1, data['N'] + 1)) >= data['MinMemory'], "Memory_Lower_Limit"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if data['IsWorkstation'][i - 1]) <= data['DemandWS'], "WS_Systems_Demand"
problem += pulp.lpSum(x[i] for i in range(1, data['N'] + 1) if not data['IsWorkstation'][i - 1]) <= data['DemandGP'], "GP_Systems_Demand"
for i in range(1, data['N'] + 1):
    problem += x[i] <= data['Demand'][i - 1], f"Demand_for_system_{i}"
    problem += x[i] >= data['Preorder'][i - 1], f"Preorders_for_system_{i}"

# Alternative memory constraints
problem += pulp.lpSum((data['MemoryBoards'][i - 1] if data['AltCompatible'][i - 1] else 0) * x[i] for i in range(1, data['N'] + 1)) <= data['AltMemory'], "Alternative_Memory_Limit"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')