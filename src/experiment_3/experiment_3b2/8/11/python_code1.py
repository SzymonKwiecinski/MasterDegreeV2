import pulp

# Given data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5, 
    'SwitchCost': 10
}

T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define decision variables
s = pulp.LpVariable.dicts("s", range(T + 1), lowBound=0)  # Storage variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0)      # Delivery variables

# Objective function
problem += pulp.lpSum(storage_cost * s[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * (x[i + 1] - x[i]) for i in range(T - 1)) + \
           pulp.lpSum(switch_cost * (x[i] - x[i + 1]) for i in range(T - 1)), "Total_Cost"

# Constraints
problem += (s[0] == 0, "Initial_Inventory")

for i in range(T):
    if i > 0:
        problem += (s[i - 1] + x[i] == deliveries[i] + s[i], f"Inventory_Balance_{i}")
    else:
        problem += (s[i - 1] + x[i] == deliveries[i] + s[i], f"Inventory_Balance_{i}")

problem += (s[T] == 0, "Ending_Inventory")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')