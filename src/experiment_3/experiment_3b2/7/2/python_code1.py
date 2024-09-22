import pulp
import json

# Data (usually you would load this from a file or another source)
data_json = """
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
"""
data = json.loads(data_json)

# Model
problem = pulp.LpProblem("DEC_Production_Plan", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Number of systems to produce
mem_used_alt = pulp.LpVariable.dicts("mem_used_alt", range(data['N']), lowBound=0)  # Alternative memory used

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"  # Naming the objective

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"  # CPU constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"  # Max disk drives constraint
problem += pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"  # Min disk drives constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) - pulp.lpSum(mem_used_alt[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"  # 256K memory max constraint
problem += pulp.lpSum(data['MemoryBoards'][i] * x[i] for i in range(data['N'])) - pulp.lpSum(mem_used_alt[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"  # 256K memory min constraint

# GP and WS demand constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"  # GP demand constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_Demand_Constraint"  # WS demand constraint

# Fulfill preorders
for i in range(data['N']):
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"  # Preorder constraint

# Individual demand constraints
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Individual_Demand_Constraint_{i}"  # Individual demand constraints

# Alternative memory non-excess constraint
for i in range(data['N']):
    problem += mem_used_alt[i] <= data['MemoryBoards'][i] * x[i], f"Non_Excess_Memory_Constraint_{i}"  # Alternative memory non-excess constraint

# Compatibility constraint
for i in range(data['N']):
    problem += mem_used_alt[i] <= data['MemoryBoards'][i] * x[i] * data['AltCompatible'][i], f"Compatibility_Constraint_{i}"  # Compatibility constraint

# Alternative memory supply constraint
problem += pulp.lpSum(mem_used_alt[i] for i in range(data['N'])) <= data['AltMemory'], "Alt_Memory_Supply_Constraint"  # Alternative memory supply constraint

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')