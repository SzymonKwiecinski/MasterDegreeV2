import pulp
import json

# Data input
data = json.loads('{"N": 5, "IsWorkstation": [false, false, false, true, true], "Price": [60000, 40000, 30000, 30000, 15000], "DiskDrives": [0.3, 1.7, 0, 1.4, 0], "MemoryBoards": [4, 2, 2, 2, 1], "Demand": [1800, 999999, 300, 999999, 999999], "Preorder": [0, 500, 0, 500, 400], "AltCompatible": [true, false, false, false, false], "MaxCpu": 7000, "MinDisk": 3000, "MaxDisk": 7000, "MinMemory": 8000, "MaxMemory": 16000, "DemandGP": 3800, "DemandWS": 3200, "AltMemory": 4000}')

# Problem
problem = pulp.LpProblem("DEC_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x_vars = [pulp.LpVariable(f"x_{i}", lowBound=data["Preorder"][i], cat='Integer') for i in range(data["N"])]

# Objective Function
profit = pulp.lpSum([data["Price"][i] * x_vars[i] for i in range(data["N"])])
problem += profit

# Constraints
problem += pulp.lpSum(x_vars) <= data["MaxCpu"], "CPU_Constraint"
problem += pulp.lpSum([data["DiskDrives"][i] * x_vars[i] for i in range(data["N"])]) >= data["MinDisk"], "Min_Disk_Constraint"
problem += pulp.lpSum([data["DiskDrives"][i] * x_vars[i] for i in range(data["N"])]) <= data["MaxDisk"], "Max_Disk_Constraint"
problem += pulp.lpSum([data["MemoryBoards"][i] * x_vars[i] for i in range(data["N"])]) >= data["MinMemory"], "Min_Memory_Constraint"
problem += pulp.lpSum([data["MemoryBoards"][i] * x_vars[i] for i in range(data["N"])]) <= data["MaxMemory"], "Max_Memory_Constraint"

# Demand constraints for each system
for i in range(data["N"]):
    problem += x_vars[i] <= data["Demand"][i], f"Demand_Constraint_{i}"

# Demand constraints for GP and WS families
problem += pulp.lpSum([x_vars[i] for i in range(data["N"]) if not data["IsWorkstation"][i]]) <= data["DemandGP"], "GP_Demand_Constraint"
problem += pulp.lpSum([x_vars[i] for i in range(data["N"]) if data["IsWorkstation"][i]]) <= data["DemandWS"], "WS_Demand_Constraint"

# Alternative memory boards usage
problem += pulp.lpSum([data["AltCompatible"][i] * x_vars[i] for i in range(data["N"])]) <= data["AltMemory"], "Alt_Memory_Constraint"

# Solve the linear program
problem.solve()

# Output Results
system_output = [(f"x_{i}", x_vars[i].varValue) for i in range(data["N"])]
profit_value = pulp.value(problem.objective)

print("system_output:", system_output)
print(f' (Objective Value): <OBJ>{profit_value}</OBJ>')