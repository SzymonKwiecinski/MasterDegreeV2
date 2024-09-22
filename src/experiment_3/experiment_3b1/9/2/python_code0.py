import pulp
import json

# Data in JSON format
data_json = '''
{
    "N": 5,
    "IsWorkstation": [false, false, false, true, true],
    "Price": [60000, 40000, 30000, 30000, 15000],
    "DiskDrives": [0.3, 1.7, 0, 1.4, 0],
    "MemoryBoards": [4, 2, 2, 2, 1],
    "Demand": [1800, 999999, 300, 999999, 999999],
    "Preorder": [0, 500, 0, 500, 400],
    "AltCompatible": [true, false, false, false, false],
    "MaxCpu": 7000,
    "MinDisk": 3000,
    "MaxDisk": 7000,
    "MinMemory": 8000,
    "MaxMemory": 16000,
    "DemandGP": 3800,
    "DemandWS": 3200,
    "AltMemory": 4000
}
'''
data = json.loads(data_json)

# Model
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Number of systems produced
mem_used = pulp.LpVariable.dicts("mem_used", range(data['N']), lowBound=0)
alt_used = pulp.LpVariable.dicts("alt_used", range(data['N']), lowBound=0)
disk_used = pulp.LpVariable.dicts("disk_used", range(data['N']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Limit"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Supply"
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Supply"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Supply"
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Supply"

for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"

problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "Workstation_Demand"
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "General-purpose_Demand"

for i in range(data['N']):
    problem += mem_used[i] <= data['MemoryBoards'][i] * x[i], f"Memory_Usage_{i}"
    problem += disk_used[i] <= data['DiskDrives'][i] * x[i], f"Disk_Usage_{i}"
    if data['AltCompatible'][i]:
        problem += alt_used[i] <= data['AltMemory'], f"Alternative_Memory_Usage_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')