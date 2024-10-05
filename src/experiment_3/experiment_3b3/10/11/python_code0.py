import pulp

# Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_and_Inventory_Schedule", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([storage_cost * I[i] for i in range(1, T + 1)]) + \
          pulp.lpSum([switch_cost * (pulp.lpSum([pulp.lpMax([x[i + 1] - x[i], x[i] - x[i + 1]]), 0])) for i in range(1, T)])

# Constraints

# Initial Inventory
problem += I[0] == 0, "Initial_Inventory"

# Inventory Balance
for i in range(1, T + 1):
    problem += I[i] == (I[i - 1] if i > 1 else 0) + x[i] - deliver[i - 1], f"Inventory_Balance_{i}"

# Final Inventory
problem += I[T] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')