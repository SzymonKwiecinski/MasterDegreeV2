import pulp

# Define the data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Production_and_Storage_Costs", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f"inventory{i}", lowBound=0, cat='Continuous') for i in range(T)]

# Objective function
problem += (pulp.lpSum(storage_cost * inventory[i] for i in range(T)) +
            pulp.lpSum(switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(T-1))), "Total Cost"

# Constraints
problem += x[0] - deliver[0] == inventory[0], "Initial Inventory Constraint"
for i in range(1, T):
    problem += inventory[i-1] + x[i] - deliver[i] == inventory[i], f"Inventory Constraint Month {i+1}"

# Solve the problem
problem.solve()

# Extract the results
x_values = [pulp.value(x[i]) for i in range(T)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {"x": x_values, "cost": total_cost}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')