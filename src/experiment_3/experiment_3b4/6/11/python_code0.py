import pulp

# Define the data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Define the problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Define the objective function
storage_costs = pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1))
switch_costs = pulp.lpSum(data['SwitchCost'] * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, data['T']))
problem += storage_costs + switch_costs

# Define the constraints
# Initial inventory is assumed to be zero, we add an auxiliary variable for I_0
I_0 = 0

# Inventory balance constraints
for i in range(1, data['T'] + 1):
    if i == 1:
        problem += I_0 + x[i] == data['Deliver'][i - 1] + I[i]
    else:
        problem += I[i - 1] + x[i] == data['Deliver'][i - 1] + I[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')