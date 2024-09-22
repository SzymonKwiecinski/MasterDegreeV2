import pulp

# Data from JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Create the Linear Program
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['T'])]  # Production variables
I = [pulp.LpVariable(f'I_{i}', lowBound=0) for i in range(data['T'])]  # Inventory variables

# Objective Function
cost_expr = pulp.lpSum(data['StorageCost'] * I[i] for i in range(data['T'])) + \
            pulp.lpSum(data['SwitchCost'] * (x[i] - x[i - 1]) for i in range(1, data['T']))
problem += cost_expr

# Constraints

# Inventory balance constraints
for i in range(data['T']):
    if i == 0:
        problem += I[i] == x[i] - data['Deliver'][i]  # Initial inventory condition
    else:
        problem += I[i] == I[i - 1] + x[i] - data['Deliver'][i]

# Final inventory constraint
problem += I[data['T'] - 1] == 0  # No leftover inventory at the end

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')