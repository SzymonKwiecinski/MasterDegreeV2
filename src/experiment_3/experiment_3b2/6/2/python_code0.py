import pulp

# Data from the provided JSON
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

# Initialize the problem
problem = pulp.LpProblem("DEC_Production_Plan", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
d = pulp.LpVariable.dicts("d", range(data['N']), lowBound=0, cat='Continuous')
m_256K = pulp.LpVariable.dicts("m_256K", range(data['N']), lowBound=0, cat='Continuous')
m_alt = pulp.LpVariable.dicts("m_alt", range(data['N']), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])), "Total_Profit"

# Constraints
problem += pulp.lpSum(x[i] for i in range(data['N'])) <= data['MaxCpu'], "CPU_Constraint"
problem += pulp.lpSum(d[i] for i in range(data['N'])) >= data['MinDisk'], "Min_Disk_Constraint"
problem += pulp.lpSum(d[i] for i in range(data['N'])) <= data['MaxDisk'], "Max_Disk_Constraint"
problem += pulp.lpSum(m_256K[i] + m_alt[i] for i in range(data['N'])) >= data['MinMemory'], "Min_Memory_Constraint"
problem += pulp.lpSum(m_256K[i] + m_alt[i] for i in range(data['N'])) <= data['MaxMemory'], "Max_Memory_Constraint"
problem += pulp.lpSum(m_alt[i] for i in range(data['N'])) <= data['AltMemory'], "Alt_Memory_Constraint"

# Maximum Demand per System
for i in range(data['N']):
    problem += x[i] <= data['Demand'][i], f"Max_Demand_Constraint_{i}"
    problem += x[i] >= data['Preorder'][i], f"Preorder_Fulfillment_Constraint_{i}"

# GP Family Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if not data['IsWorkstation'][i]) <= data['DemandGP'], "GP_Demand_Constraint"

# WS Family Demand Constraint
problem += pulp.lpSum(x[i] for i in range(data['N']) if data['IsWorkstation'][i]) <= data['DemandWS'], "WS_Demand_Constraint"

# System-specific Resource Usage
for i in range(data['N']):
    problem += d[i] == data['DiskDrives'][i] * x[i], f"Disk_Usage_Constraint_{i}"
    problem += m_256K[i] + m_alt[i] == data['MemoryBoards'][i] * x[i], f"Memory_Usage_Constraint_{i}"
    
    # Alternative Memory Compatibility
    if not data['AltCompatible'][i]:
        problem += m_alt[i] == 0, f"Alt_Memory_Compatibility_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')