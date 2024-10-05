import pulp

# Data from the problem
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extract data variables
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
s = [pulp.LpVariable(f's_{i}', lowBound=0, cat='Continuous') for i in range(T)]
delta = [pulp.LpVariable(f'delta_{i}', lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective function
total_storage_cost = pulp.lpSum(storage_cost * s[i] for i in range(T))
total_switch_cost = pulp.lpSum(switch_cost * delta[i] for i in range(T-1))
problem += total_storage_cost + total_switch_cost, "Total_Cost"

# Constraints
# Initial inventory is zero
problem += s[0] == x[0] - deliver[0], "Inventory_Initial"

# Inventory balance for subsequent months
for i in range(1, T):
    problem += s[i] == s[i-1] + x[i] - deliver[i], f"Inventory_Balance_{i}"

# Constraints for the switch costs (linearization)
for i in range(T-1):
    problem += delta[i] >= x[i] - x[i+1], f"Switch_Cost_Constraint_Positive_{i}"
    problem += delta[i] >= x[i+1] - x[i], f"Switch_Cost_Constraint_Negative_{i}"

# Solve the problem
problem.solve()

# Collect results
x_values = [pulp.value(x[i]) for i in range(T)]
cost = pulp.value(problem.objective)

# Output format
output = {
    "x": x_values,
    "cost": cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')