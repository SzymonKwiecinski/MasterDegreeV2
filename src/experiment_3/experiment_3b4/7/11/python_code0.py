import pulp

# Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Time periods
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]
I = [pulp.LpVariable(f'I_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]

# Initial inventory
I0 = 0

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * abs(x[i + 1] - x[i]) for i in range(T - 1))

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + I0 == deliveries[i] + I[i], f'Inventory_Balance_{i+1}'
    else:
        problem += x[i] + I[i-1] == deliveries[i] + I[i], f'Inventory_Balance_{i+1}'

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')