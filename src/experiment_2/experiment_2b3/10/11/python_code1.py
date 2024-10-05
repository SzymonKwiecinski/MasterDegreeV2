import pulp

# Extract data from JSON
data = {
    "T": 12, 
    "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    "StorageCost": 5, 
    "SwitchCost": 10
}

T = data["T"]
deliver = data["Deliver"]
storage_cost = data["StorageCost"]
switch_cost = data["SwitchCost"]

# Create the LP problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f"inventory_{i}", lowBound=0, cat='Continuous') for i in range(T)]

# Auxiliary variables for the switch cost
d_plus = [pulp.LpVariable(f"d_plus_{i}", lowBound=0, cat='Continuous') for i in range(T-1)]
d_minus = [pulp.LpVariable(f"d_minus_{i}", lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective function
total_cost = (
    pulp.lpSum(storage_cost * inventory[i] for i in range(T)) +
    pulp.lpSum(switch_cost * (d_plus[i] + d_minus[i]) for i in range(T-1))
)

problem += total_cost

# Constraints
problem += (inventory[0] == x[0] - deliver[0])  # Initial inventory
for i in range(1, T):
    problem += (inventory[i] == inventory[i-1] + x[i] - deliver[i])

for i in range(T-1):
    problem += (x[i+1] - x[i] <= d_plus[i])  # d_plus captures positive change
    problem += (x[i] - x[i+1] <= d_minus[i])  # d_minus captures negative change

# Solve the problem
problem.solve()

# Extract the results
production_plan = [pulp.value(x[i]) for i in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "x": production_plan,
    "cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')