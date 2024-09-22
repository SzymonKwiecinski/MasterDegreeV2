import pulp

# Parse the data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data["T"]
deliver = data["Deliver"]
storage_cost = data["StorageCost"]
switch_cost = data["SwitchCost"]

# Define the Linear Program
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f'inv_{i}', lowBound=0, cat='Continuous') for i in range(T)]
switch = [pulp.LpVariable(f'switch_{i}', lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + pulp.lpSum(switch_cost * switch[i] for i in range(T-1))

# Add the objective to the problem
problem += total_cost

# Constraints
# Inventory balance constraints
problem += (x[0] - deliver[0] == inventory[0], "Inventory_Balance_Month_1")
for i in range(1, T):
    problem += (x[i] + inventory[i-1] - deliver[i] == inventory[i], f"Inventory_Balance_Month_{i+1}")

# Switch constraints to handle absolute difference
for i in range(T-1):
    problem += (x[i+1] - x[i] <= switch[i], f"Switch_Positive_{i+1}")
    problem += (x[i] - x[i+1] <= switch[i], f"Switch_Negative_{i+1}")

# Solve the problem
problem.solve()

# Prepare the output
output = {"x": [pulp.value(x[i]) for i in range(T)], 
          "cost": pulp.value(problem.objective)}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')