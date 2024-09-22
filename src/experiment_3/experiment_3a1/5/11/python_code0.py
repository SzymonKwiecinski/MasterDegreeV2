import pulp

# Data from JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Number of months
T = data['T']
Deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)  # Production levels
I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0)  # Inventory levels

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (x[i + 1] - x[i]) 
                      for i in range(1, T)) + storage_cost * I[T], "Total_Cost"

# Constraints
problem += I[1] == x[1] - Deliver[0], "Inventory_1"
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - Deliver[i - 1], f"Inventory_{i}"

# Additional constraints
for i in range(1, T + 1):
    problem += I[i] >= 0, f"NonNegativity_Inventory_{i}"
problem += I[T] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')