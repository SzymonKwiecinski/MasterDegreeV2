import pulp

# Load data from JSON format
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f"inventory_{i}", lowBound=0, cat='Continuous') for i in range(T)]

# Objective function
switching_costs = [switch_cost * abs(x[i] - x[i-1]) for i in range(1, T)]
total_switching_cost = pulp.lpSum(switching_costs)
total_storage_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)])
problem += total_switching_cost + total_storage_cost

# Constraints
# Initial inventory is zero
problem += inventory[0] == x[0] - deliver[0]

# Inventory balance constraints
for i in range(1, T):
    problem += inventory[i] == inventory[i-1] + x[i] - deliver[i]

# Solve the problem
problem.solve()

# Print results
result = {"x": [pulp.value(x[i]) for i in range(T)], "cost": pulp.value(problem.objective)}
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
result