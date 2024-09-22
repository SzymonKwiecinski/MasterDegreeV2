import pulp

# Parsing the data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f"inventory_{i}", lowBound=0, cat='Continuous') for i in range(T)]
z = [pulp.LpVariable(f"z_{i}", lowBound=0, cat='Continuous') for i in range(T - 1)]

# Objective function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * z[i] for i in range(T - 1)])

problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        # Start with zero inventory
        problem += (x[i] - deliver[i] == inventory[i])
    else:
        # Inventory balance constraints
        problem += (x[i] + inventory[i-1] - deliver[i] == inventory[i])

# Additional constraints for the switch cost
for i in range(T - 1):
    problem += x[i+1] - x[i] <= z[i]
    problem += x[i] - x[i+1] <= z[i]

# Solve the problem
problem.solve()

# Fetching results
production_schedule = [pulp.value(x[i]) for i in range(T)]
total_cost_value = pulp.value(problem.objective)

# Printing the objective
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')