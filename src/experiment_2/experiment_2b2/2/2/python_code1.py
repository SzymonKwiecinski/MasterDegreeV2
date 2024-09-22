import pulp
import json

# Problem definition
problem = pulp.LpProblem("DEC_Production_Max_Profit", pulp.LpMaximize)

# Data
data = {
    "N": 5,
    "IsWorkstation": [False, False, False, True, True],
    "Price": [60000, 40000, 30000, 30000, 15000],
    "DiskDrives": [0.3, 1.7, 0, 1.4, 0],
    "MemoryBoards": [4, 2, 2, 2, 1],
    "Demand": [1800, 999999, 300, 999999, 999999],
    "Preorder": [0, 500, 0, 500, 400],
    "AltCompatible": [True, False, False, False, False],
    "MaxCpu": 7000,
    "MinDisk": 3000,
    "MaxDisk": 7000,
    "MinMemory": 8000,
    "MaxMemory": 16000,
    "DemandGP": 3800,
    "DemandWS": 3200,
    "AltMemory": 4000
}

# Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=data["Preorder"][i]) for i in range(data["N"])]
mem_used = [pulp.LpVariable(f"mem_used_{i}", lowBound=0) for i in range(data["N"])]
alt_mem_used = [pulp.LpVariable(f"alt_mem_used_{i}", lowBound=0) for i in range(data["N"])]
disk_used = [pulp.LpVariable(f"disk_used_{i}", lowBound=0) for i in range(data["N"])]

# Objective
problem += pulp.lpSum([x[i] * data["Price"][i] for i in range(data["N"])]), "Total_Profit"

# Constraints
# CPU constraint
problem += pulp.lpSum(x) <= data["MaxCpu"], "CPU_Limit"

# Disk constraints
problem += pulp.lpSum(disk_used) >= data["MinDisk"], "Min_Disk"
problem += pulp.lpSum(disk_used) <= data["MaxDisk"], "Max_Disk"

# Memory constraints
problem += pulp.lpSum(mem_used) >= data["MinMemory"], "Min_Memory"
problem += pulp.lpSum(mem_used) <= data["MaxMemory"], "Max_Memory"

# Alternative memory constraints
problem += pulp.lpSum(alt_mem_used) <= data["AltMemory"], "Alt_Memory_Limit"

# Demand constraints
problem += pulp.lpSum([x[i] for i in range(data["N"]) if not data["IsWorkstation"][i]]) <= data["DemandGP"], "Demand_GP"
problem += pulp.lpSum([x[i] for i in range(data["N"]) if data["IsWorkstation"][i]]) <= data["DemandWS"], "Demand_WS"

# Individual constraints
for i in range(data["N"]):
    problem += x[i] <= data["Demand"][i], f"Demand_{i}"
    problem += mem_used[i] + alt_mem_used[i] == x[i] * data["MemoryBoards"][i], f"MemoryBoard_Usage_{i}"
    problem += disk_used[i] == x[i] * data["DiskDrives"][i], f"DiskDrive_Usage_{i}"

    if not data["AltCompatible"][i]:
        problem += alt_mem_used[i] == 0, f"Alt_Memory_Usage_Restriction_{i}"

# Solve the problem
problem.solve()

# Prepare results
system_output = [{
    "num_produced": x[i].varValue,
    "total_256K_boards_used": mem_used[i].varValue,
    "total_alt_boards_used": alt_mem_used[i].varValue,
    "total_disk_drives_used": disk_used[i].varValue
} for i in range(data["N"])]

profit = pulp.value(problem.objective)

output = {
    "system_output": system_output,
    "profit": profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')