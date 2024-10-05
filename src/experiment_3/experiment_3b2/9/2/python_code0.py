import pulp
import json

# Data provided
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

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Continuous
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=0)  # Continuous
z = pulp.LpVariable.dicts("z", range(data['N']), cat='Binary')  # Binary

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "Max_CPU_Constraint"
problem += (data['MinDisk'] <= pulp.lpSum(data['DiskDrives'][i] * x[i] for i in range(data['N'])) <= data['MaxDisk'], "Disk_Drive_Constraint")
problem += (data['MinMemory'] <= pulp.lpSum(y[i] for i in range(data['N'])) <= data['MaxMemory'], "Memory_Constraint")
problem += pulp.lpSum(z[i] for i in range(data['N'])) <= data['AltMemory'], "Alternative_Memory_Constraint"

for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Demand_Constraint_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_Constraint_{i}"
    problem += y[i] == data['MemoryBoards'][i] * x[i], f"Memory_Usage_Constraint_{i}"

# GP and WS Constraints
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_Demand_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')