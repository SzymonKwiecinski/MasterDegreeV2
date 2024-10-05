import pulp

# Given data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Unpacking the data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a LP minimization problem
problem = pulp.LpProblem("ProductionPlanning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Produce", range(1, T + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
total_cost = (
    pulp.lpSum([storage_cost * I[i] for i in range(1, T + 1)]) +
    pulp.lpSum([switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T)])
)

problem += total_cost

# Constraints

# Initial inventory
problem += I[1] - x[1] == -deliver[0], "Initial_Inventory"

# Inventory balance and non-negativity
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1], f"Inventory_Balance_{i}"

# Final inventory
problem += I[T] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')