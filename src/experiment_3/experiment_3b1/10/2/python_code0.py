import pulp
import json

# Input data
data = json.loads("{'N': 5, 'IsWorkstation': [False, False, False, True, True], 'Price': [60000, 40000, 30000, 30000, 15000], 'DiskDrives': [0.3, 1.7, 0, 1.4, 0], 'MemoryBoards': [4, 2, 2, 2, 1], 'Demand': [1800, 999999, 300, 999999, 999999], 'Preorder': [0, 500, 0, 500, 400], 'AltCompatible': [True, False, False, False, False], 'MaxCpu': 7000, 'MinDisk': 3000, 'MaxDisk': 7000, 'MinMemory': 8000, 'MaxMemory': 16000, 'DemandGP': 3800, 'DemandWS': 3200, 'AltMemory': 4000}")

N = data['N']
is_workstation = data['IsWorkstation']
price = data['Price']
disk = data['DiskDrives']
mem = data['MemoryBoards']
demand = data['Demand']
preorder = data['Preorder']
alt_mem = data['AltMemory']
alt_compatible = data['AltCompatible']

max_cpu = data['MaxCpu']
min_disk = data['MinDisk']
max_disk = data['MaxDisk']
min_mem = data['MinMemory']
max_mem = data['MaxMemory']
demand_gp = data['DemandGP']
demand_ws = data['DemandWS']

# Costs (assuming hypothetical values for cost_mem and cost_disk)
cost_mem = 1000
cost_disk = 500

# Problem Definition
problem = pulp.LpProblem("DEC_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)  # Continuous for systems produced
y = pulp.LpVariable.dicts("y", range(N), lowBound=0, cat='Integer')  # Integer for alternative memory boards

# Objective Function
profit = pulp.lpSum(price[i] * x[i] for i in range(N)) - \
         pulp.lpSum(cost_mem * (mem[i] * x[i] - y[i]) for i in range(N)) - \
         pulp.lpSum(cost_disk * disk[i] * x[i] for i in range(N))

problem += profit

# Constraints
problem += pulp.lpSum(x[i] for i in range(N)) <= max_cpu  # CPU availability
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) >= min_disk  # Minimum disk drives
problem += pulp.lpSum(disk[i] * x[i] for i in range(N)) <= max_disk  # Maximum disk drives
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) >= min_mem  # Minimum memory boards
problem += pulp.lpSum(mem[i] * x[i] for i in range(N)) <= max_mem  # Maximum memory boards

for i in range(N):
    problem += x[i] >= preorder[i]  # Satisfy preorders

# Demand constraints for GP and WS families
problem += pulp.lpSum(x[i] for i in range(N) if not is_workstation[i]) <= demand_gp  # GP family demand
problem += pulp.lpSum(x[i] for i in range(N) if is_workstation[i]) <= demand_ws  # WS family demand

for i in range(N):
    problem += y[i] <= alt_mem  # Alternative memory board limitation
    if alt_compatible[i]:
        problem += y[i] <= pulp.lpSum(mem[j] * x[j] for j in range(N))  # Alternative memory board compatibility

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')