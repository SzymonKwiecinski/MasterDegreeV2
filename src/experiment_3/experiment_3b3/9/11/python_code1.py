import pulp

# Extract data from JSON
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f"I_{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]

# Objective function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (x[i+1] - x[i]) 
                      for i in range(T-1)) + storage_cost * I[T-1], "Total_Cost"

# Constraints
# Inventory balance constraints
for i in range(T):
    if i == 0:
        problem += I[i] == x[i] - deliver[i], f"Inventory_Balance_{i+1}"
    else:
        problem += I[i] == I[i-1] + x[i] - deliver[i], f"Inventory_Balance_{i+1}"

# No inventory carry over at the end of last month
problem += I[T-1] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Output the results
print("Production plan (x):")
for i in range(T):
    print(f"Month {i+1}: {x[i].varValue}")

print(f'Total minimized cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')