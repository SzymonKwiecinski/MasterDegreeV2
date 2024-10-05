import pulp

# Problem data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Defining the LP problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize storage cost and switching cost
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T))

# Adding switching costs correctly
for i in range(T-1):
    total_cost += switch_cost * (x[i+1] - x[i]) if x[i+1] >= x[i] else switch_cost * (x[i] - x[i+1])

problem += total_cost

# Constraints
# Initial inventory
problem += inventory[0] == x[0] - deliver[0]

# Monthly inventory balance
for i in range(1, T):
    problem += inventory[i] == inventory[i-1] + x[i] - deliver[i]

# Solve the problem
problem.solve()

# Collect the result
result = {'x': [pulp.value(x[i]) for i in range(T)], 'cost': pulp.value(problem.objective)}

# Print the results
print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')