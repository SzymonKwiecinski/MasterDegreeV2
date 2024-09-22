import pulp

# Data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

# Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Decision variables
x = [pulp.LpVariable(f"x_{i+1}", lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f"inventory_{i+1}", lowBound=0, cat='Continuous') for i in range(T)]
abs_diff = [pulp.LpVariable(f"abs_diff_{i+1}", lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)])
switch_costs = pulp.lpSum([switch_cost * abs_diff[i] for i in range(T-1)])
problem += total_cost + switch_costs

# Constraints
# Initial inventory
problem += inventory[0] == x[0] - deliver[0]

# Inventory balance constraints
for i in range(1, T):
    problem += inventory[i] == inventory[i-1] + x[i] - deliver[i]

# Absolute difference constraints
for i in range(T-1):
    problem += abs_diff[i] >= x[i+1] - x[i]
    problem += abs_diff[i] >= x[i] - x[i+1]

# Solve
problem.solve()

# Results
production_plan = [pulp.value(x[i]) for i in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "x": production_plan,
    "cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')