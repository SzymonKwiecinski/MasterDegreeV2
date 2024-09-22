import pulp

# Data provided
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Variables from the data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Problem definition
problem = pulp.LpProblem("Minimize_Storage_and_Switch_Cost", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
I = [pulp.LpVariable(f'I_{i}', lowBound=0, cat='Continuous') for i in range(T)]
y = [pulp.LpVariable(f'y_{i}', lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective Function
problem += pulp.lpSum([storage_cost * I[i] for i in range(T)]) + \
           pulp.lpSum([switch_cost * y[i] for i in range(T-1)])

# Constraints
problem += I[0] == 0, "Initial Inventory"

for i in range(T):
    problem += x[i] + (I[i-1] if i > 0 else 0) == deliver[i] + I[i], f"Inventory_Balance_{i}"

for i in range(T-1):
    problem += y[i] >= x[i+1] - x[i], f"Switch_Constraint_Positive_{i}"
    problem += y[i] >= x[i] - x[i+1], f"Switch_Constraint_Negative_{i}"

# Solving the problem
problem.solve()

# Output the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")