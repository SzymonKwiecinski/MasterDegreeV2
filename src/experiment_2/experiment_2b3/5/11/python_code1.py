import pulp

# Parse the input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the LP problem
problem = pulp.LpProblem("Inventory_Optimization", pulp.LpMinimize)

# Decision variables: x[i] is the production in month i, s[i] is the inventory at the end of month i
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize storage costs and switching costs
storage_cost_part = pulp.lpSum([storage_cost * s[i] for i in range(T)])
switch_cost_part = pulp.lpSum([switch_cost * (x[i+1] - x[i]) for i in range(T-1)])  # Remove lpAbs, calculate switching directly
problem += storage_cost_part + switch_cost_part

# Constraints
# Initial inventory is zero
problem += s[0] == 0

# Balancing demand and production with inventory
for i in range(T):
    problem += x[i] + (s[i-1] if i > 0 else 0) == deliver[i] + s[i]

# Solver
problem.solve()

# Extract solution
production_schedule = [pulp.value(x[i]) for i in range(T)]
total_cost = pulp.value(problem.objective)

# Format output as specified
output = {
    "x": production_schedule,
    "cost": total_cost,
}

# Print final objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')