import pulp
import json

# Load the data from the provided JSON format
data = json.loads("""
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
""")

# Problem Initialization
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision Variables
num_produced = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(data['N'])]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0) for i in range(data['N'])]
alt_used = [pulp.LpVariable(f"alt_used_{i}", lowBound=0) for i in range(data['N'])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0) for i in range(data['N'])]

# Objective Function
profit = pulp.lpSum([num_produced[i] * data['Price'][i] for i in range(data['N'])])
problem += profit

# Constraints
# CPU constraint
problem += pulp.lpSum(num_produced) <= data['MaxCpu']

# Memory constraints
problem += pulp.lpSum(mem_used) >= data['MinMemory']
problem += pulp.lpSum(mem_used) <= data['MaxMemory']
problem += pulp.lpSum(alt_used) <= data['AltMemory']

# Disk constraints
problem += pulp.lpSum(disk_used) >= data['MinDisk']
problem += pulp.lpSum(disk_used) <= data['MaxDisk']

# Demand and Preorder constraints
for i in range(data['N']):
    problem += num_produced[i] <= data['Demand'][i]
    problem += num_produced[i] >= data['Preorder'][i]
    problem += mem_used[i] == num_produced[i] * data['MemoryBoards'][i]
    problem += disk_used[i] == num_produced[i] * data['DiskDrives'][i]
    if data['AltCompatible'][i]:
        problem += mem_used[i] + alt_used[i] == num_produced[i] * data['MemoryBoards'][i]
    else:
        problem += alt_used[i] == 0

# General Purpose and Workstation demand constraints
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if not data['IsWorkstation'][i]]) <= data['DemandGP']
problem += pulp.lpSum([num_produced[i] for i in range(data['N']) if data['IsWorkstation'][i]]) <= data['DemandWS']

# Solve the problem
problem.solve()

# Preparing the output
system_output = [
    {
        "num_produced": pulp.value(num_produced[i]),
        "total_256K_boards_used": pulp.value(mem_used[i]),
        "total_alt_boards_used": pulp.value(alt_used[i]),
        "total_disk_drives_used": pulp.value(disk_used[i])
    }
    for i in range(data['N'])
]

output = {
    "system_output": system_output,
    "profit": pulp.value(problem.objective)
}

print(json.dumps(output, indent=2))

# Objective value print
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')