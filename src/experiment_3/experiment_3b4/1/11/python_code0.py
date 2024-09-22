import pulp

# Data from the JSON format
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

# Create the Linear Programming Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]
s = [pulp.LpVariable(f's_{i}', lowBound=0, cat='Continuous') for i in range(1, T + 1)]
switch = [pulp.LpVariable(f'switch_{i}', lowBound=0, cat='Continuous') for i in range(1, T)]

# Objective Function
problem += pulp.lpSum(storage_cost * s[i] for i in range(T)) + pulp.lpSum(switch_cost * switch[i] for i in range(T - 1))

# Constraints
# Inventory balance constraints
problem += s[0] == x[0] - deliver[0]  # for the first month
for i in range(1, T):
    problem += s[i] == s[i - 1] + x[i] - deliver[i]

# Linearizing absolute value of production change for switch costs
for i in range(T - 1):
    problem += x[i + 1] - x[i] <= switch[i]
    problem += x[i] - x[i + 1] <= switch[i]

# Initial inventory is zero
problem += s[0] == x[0] - deliver[0]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')