import pulp

# Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create an LP problem
problem = pulp.LpProblem("Production_Inventory_Scheduling", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f'I{i}', lowBound=0, cat='Continuous') for i in range(1, T+1)]

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (pulp.lpSum([pulp.lpDot([1, -1], [x[i+1], x[i]])]) if i < T - 1 else 0) for i in range(T))

# Constraints
# Inventory balance for each month
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] == I[i]
    else:
        problem += I[i-1] + x[i] - deliver[i] == I[i]

# Inventory must be zero at the end of the year
problem += I[T-1] == 0

# Solve the problem
problem.solve()

# Output the value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')