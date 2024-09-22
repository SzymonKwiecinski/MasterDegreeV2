import pulp

# Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Create the model
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0)
I = pulp.LpVariable.dicts("Inventory", range(0, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
           pulp.lpSum(data['SwitchCost'] * (x[i] - x[i-1]) for i in range(2, data['T'] + 1))

# Constraints
problem += I[0] == 0  # Initial inventory is zero

for i in range(1, data['T'] + 1):
    if i == 1:
        problem += I[i] == x[i] - data['Deliver'][i-1]  # For the first month
    else:
        problem += I[i] == I[i-1] + x[i] - data['Deliver'][i-1]  # Delivery requirement

# Ensure no inventory costs at the end of the year
problem += I[data['T']] == 0

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')