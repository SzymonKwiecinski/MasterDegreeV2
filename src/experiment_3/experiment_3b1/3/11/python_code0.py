import pulp

# Data provided
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Problem Definition
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Production", range(data['T']), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(data['T']), lowBound=0, cat='Continuous')

# Objective Function
switching_cost = pulp.lpSum(data['SwitchCost'] * pulp.lpSum(pulp.lpAbs(x[i+1] - x[i]) for i in range(data['T'] - 1)))
storage_cost = pulp.lpSum(data['StorageCost'] * I[i] for i in range(data['T']))
problem += switching_cost + storage_cost, "Total_Cost"

# Constraints
problem += I[0] == 0, "Initial_Inventory"

for i in range(data['T']):
    if i > 0:
        problem += I[i] == I[i-1] + x[i] - data['Deliver'][i], f"Inventory_Balance_{i}"
    else:
        problem += I[i] == x[i] - data['Deliver'][i], f"Inventory_Balance_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')